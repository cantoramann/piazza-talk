import os
import env_manager
import requests
import utils.reader as utils
import errors
from errors import InvalidPostError
import markdown_generator
from markdown_generator import MarkdownGenerator

class ClassReader():
    def __init__(self, class_url, role='instructor'):
        if class_url is None:
            raise ValueError('Class url cannot be None')
        self.class_url = class_url
        self.role = role


    def create_paths(self):
        data_dir = f"/class_data/{self.class_url}"
        raw_dir = f"{data_dir}/raw"
        embeddings_dir = f"{data_dir}/embeddings"
        # Create the raw directory if it doesn't exist
        if not os.path.exists(raw_dir):
            os.makedirs(raw_dir)
        # Create the embeddings directory if it doesn't exist
        if not os.path.exists(embeddings_dir):
            os.makedirs(embeddings_dir)
        return (raw_dir, embeddings_dir)


    def prepare_config(self):
        self.base_api_url = 'https://piazza.com/logic/api'
        self.file_paths = self.create_paths()
        self.headers = self.prepare_headers()
        self.cookies = self.prepare_cookies()
        self.params = self.prepare_params()
        self.json_params = self.prepare_json_params()


    def prepare_headers(self):
        headers = {
            'authority': env_manager.get('authority'),
            'accept':  env_manager.get('accept'),
            'accept-language':  env_manager.get('accept_language'),
            'content-type':  env_manager.get('content_type'),
            'csrf-token':  env_manager.get('csrf_token'),
            'origin': env_manager.get('origin'),
            'sec-ch-ua': env_manager.get('sec_ch_ua'),
            'sec-ch-ua-mobile': env_manager.get('sec_ch_ua_mobile'),
            'sec-ch-ua-platform': env_manager.get('sec_ch_ua_platform'),
            'sec-fetch-dest': env_manager.get('sec_fetch_dest'),
            'sec-fetch-mode': env_manager.get('sec_fetch_mode'),
            'sec-fetch-site': env_manager.get('sec_fetch_site'),
            'user-agent': env_manager.get('user_agent'),
        }
        return headers


    def prepare_cookies(self):
        cookies = {
            'session_id': env_manager.get('session_id'),
            'last_piaz_user': env_manager.get('last_piaz_user'),
            'AWSALB': env_manager.get('AWSALB'),
            'AWSALBCORS': env_manager.get('AWSALBCORS'),
            'piazza_session': env_manager.get('piazza_session'),
        }
        return cookies


    def prepare_params(self):
        params = {'method': 'content.get'}
        return params


    def prepare_json_params(self):
        # add cid from Piazza for each post retrieval
        json_params = {
            'method': 'content.get',
            'params': {
                'nid': env_manager.get("STUDENT_NID"),
                'student_view': None,
            }
        }
        return json_params


    def prepare_post_retrieval(self):
        # Make sure that the retrieval post id is updated
        self.headers['referer'] = f"{env_manager.get('referer_base')}{self.current_post_id}"
        self.json_params['params']['cid'] = str(self.current_post_id)


    def check_conditions(self):
        print('Checking conditions')
        print('Role: ', self.role)

        # max_length overrides convergence_threshold
        if self.max_length is not None:
            print('You have provided a post ID limit to stop at. Defined limit is: ', self.max_length)
        elif self.convergence_threshold is not None:
            print('You have provided a convergence threshold. Defined threshold is: ', self.convergence_threshold)
        if self.max_length is None and self.convergence_threshold is None:
            print('You have not provided a post ID limit or a convergence threshold. Defaulting to a convergence threshold of 10.')
            self.convergence_threshold = 10
        print('Checks apply. Starting to read posts...')


    def should_continue_reading(self):
        if self.max_length is not None:
            return True if self.current_post_id <= self.max_length else False
        else:
            # Read convergence threshold from environment variable manager
            return True if self.consecutive_failures < self.convergence_threshold else False


    def request_post(self):
        response = requests.post(self.base_api_url, params=self.params, cookies=self.cookies, headers=self.headers, json=self.json_params)
        return response


    def read(self):
        # If the number of posts to read is specified, from 1 to N inclusive, this will be used for failure handling
        if env_manager.get('max_length') is not None:
            self.max_length = int(env_manager.get('max_length'))
        elif env_manager.get('convergence_threshold') is not None and env_manager.get('convergence_threshold') > 0:
            self.convergence_threshold = int(env_manager.get('convergence_threshold'))
        else:
            self.convergence_threshold = 10 # Default
        
        self.check_conditions()

        self.current_post_id = 1

        # Init markdown generator
        self.markdown_generator = MarkdownGenerator()

        while self.should_continue_reading():
            try:
                self.prepare_post_retrieval()
                print(f"Reading post #{self.current_post_id}")
                response = self.request_post()
                
                if response.status_code != 200:
                    # throw an error with the message that the page is not valid with id
                    raise Exception(f"Post #{self.current_post_id} is not valid")
                
                response_json = response.json()
                if response_json['result'] == None:
                    raise Exception(f"Post #{self.current_post_id} is not valid")

                self.consecutive_failures = 0 # Reset the number of consecutive failures. Update here to avoid parsing errors to contribute to the retrieval failure count

                post_result = response_json['result']
                
                # Parse post type (question, note, poll etc)
                post_type = utils.parse_post_type(post_result)
                if post_type is None: # Not a valid post type
                    raise Exception(f"Post #{self.current_post_id} is not valid")

                # Parse post privacy
                post_privacy = post_result['status']
                if utils.is_private_post(post_privacy):
                    raise Exception(f"Post #{self.current_post_id} is private. Contunuing to next post...")
                
                # Parse post metadata
                post_title = utils.parse_post_title(post_result)
                post_main_thread = utils.parse_post_main_content(post_result)
                post_answer = utils.parse_answer(post_result)
                post_followups = utils.parse_followups(post_result)
                post_tags = utils.parse_post_tags(post_result)

                post_data = {
                    'post_id': self.current_post_id,
                    'post_type': post_type,
                    'post_title': post_title,
                    'post_main_thread': post_main_thread,
                    'post_answer': post_answer,
                    'post_followups': post_followups,
                    'post_tags': post_tags
                }

                # Generate markdown
                markdown = self.markdown_generator.generate_markdown(self.file_paths[0], post_data)

            except InvalidPostError as e:
                print(e)
                continue

            except Exception as e:
                print(e)
                self.consecutive_failures += 1 # Increment the number of consecutive failures
                continue
                
            finally:
                self.current_post_id += 1 # Increment the post ID
