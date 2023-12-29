import os
import requests
import time
import config
import utils

params = {
    'method': 'content.get',
}

json_data = {
    'method': 'content.get',
    'params': {
        'nid': config.STUDENT_NID,
        'student_view': None,
    },
}

posts_directory = "posts"
repeated_failures = 10

post_id = 779
content_valid = True

while content_valid:
    print(f"Post ID: {post_id}")
    try:
        json_data['params']['cid'] = str(post_id)
        config.headers['referer'] = f"{config.REFERER_BASE}{post_id}"

        # Make the request
        response = requests.post('https://piazza.com/logic/api', params=params, cookies=config.cookies, headers=config.headers, json=json_data)
        if response.status_code != 200:
            post_id += 1
            continue

        # Parse the JSON data
        data = response.json()

        if data['result'] == None:
            repeated_failures =+ 1
            if repeated_failures > 10:
                content_valid = False
            post_id += 1
            continue
        repeated_failures = 0

        print('\n')
        if utils.parse_post_privacy(data['result']) == 'private':
            post_id += 1
            print("----- private post, skipping -----")
            continue

        post_title = utils.parse_post_title(data['result'])
        print('post title: ', post_title, '\n\n')
        
        post_type = utils.parse_post_type(data['result'])

        if post_type == None:
            post_id += 1
            continue
        
        post_main_thread = utils.parse_post_main_content(data['result'])
        post_answer = utils.parse_answer(data['result'])
        post_followups = utils.parse_followups(data['result'])
        post_tags = utils.parse_post_tags(data['result'])
        
        with open(os.path.join(posts_directory, f"post_{post_id}.txt"), 'w') as file:
            file.write('# Title:' + post_title + '\n')
            file.write('## Post type: ' + post_type + '\n')
            
            if post_type == 'question':
                file.write('\n## Question:\n```' + post_main_thread + '```\n')
            else:
                file.write('\n## Note:\n```' + post_main_thread + '```\n')

            if post_answer != None:    
                file.write('\n## Answer:\n')            
                if post_answer[0] == 'instructor_answer':
                    file.write('### Answerer: instructor\n')
                elif post_answer[0] == 'student_answer':
                    file.write('### Answerer: student\n')
                file.write('\n### Answer Data:\n```' + post_answer[1] + '```\n')

            if post_followups != None:
                file.write('\n## Followups:\n')
                for followup in post_followups:
                    if followup == None:
                        continue
                    file.write(followup + '\n')

        with open(os.path.join(posts_directory, f"post_{post_id}_metadata.txt"), 'w') as file:
            file.write('Title:' + post_title + '\n')
            file.write('Post type: ' + post_type + '\n')
            file.write('Tags: ' + str(post_tags) + '\n')

    except Exception as e:
        print(f"An error occurred: {e}. Post ID: {post_id}")
        break

    time.sleep(1)  # Sleep for 1 second to avoid rate limiting
    post_id += 1