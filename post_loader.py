import os
import re
import weaviate
from weaviate.util import generate_uuid5

class WeaviatePostInserter:
    def __init__(self, class_name="PiazzaPosts", weaviate_port=8080, weaviate_grpc_port=50051):
        self.class_name = class_name
        self.client = self.initialize_weaviate_client(weaviate_port, weaviate_grpc_port)
        self.ensure_collection_exists()

    @staticmethod
    def initialize_weaviate_client(port, grpc_port):
        """ Initialize the Weaviate client. """
        return weaviate.connect_to_local(
            port=port,
            grpc_port=grpc_port,
            headers={"X-OpenAI-Api": os.getenv("OPENAI_API_KEY")}
        )

    @staticmethod
    def extract_number(filename):
        """ Extract number from filename for sorting. """
        match = re.search(r'\d+', filename)
        return int(match.group()) if match else 0

    def ensure_collection_exists(self):
        """ Ensure the collection exists in Weaviate, create if it does not. """
        try:
            self.client.collections.get(self.class_name)
        except weaviate.exceptions.ObjectNotFoundException:
            self.create_collection()

    def create_collection(self):
        """ Create a new collection in Weaviate. """
        self.client.collections.create(
            name=self.class_name,
            vectorizer_config=weaviate.classes.Configure.Vectorizer.text2vec_openai(),
            generative_config=weaviate.classes.Configure.Generative.openai(),
            properties=[
                weaviate.classes.Property(name="metadata", data_type=weaviate.classes.DataType.TEXT),
                weaviate.classes.Property(name="content", data_type=weaviate.classes.DataType.TEXT),
            ]
        )

    def process_and_insert_posts(self):
        """ Process post files and insert them into the Weaviate database. """
        posts = self.process_posts()
        self.insert_posts_to_db(posts)

    def process_posts(self):
        """ Process and return post objects from files. """
        posts = []
        post_data = {}
        for filename in sorted(os.listdir('posts'), key=self.extract_number):
            with open(os.path.join('posts', filename), 'r') as file:
                file_content = file.read()
                key = 'metadata' if 'metadata' in filename else 'content'
                post_data[key] = file_content

                if 'metadata' in post_data and 'content' in post_data:
                    post_object = self.create_post_object(post_data)
                    posts.append(post_object)
                    post_data.clear()
        print(f"Total entries processed: {len(posts)}")
        return posts

    @staticmethod
    def create_post_object(post_data):
        """ Create a Weaviate data object for the post. """
        properties = {"metadata": post_data['metadata'], "content": post_data['content']}
        return weaviate.classes.DataObject(
            properties=properties,
            uuid=generate_uuid5(properties)
        )

    def insert_posts_to_db(self, posts):
        """ Insert posts into the Weaviate database. """
        try:
            response = self.client.collections.get(self.class_name).data.insert_many(posts)
            print("Insert response:", response)
        except Exception as e:
            print(f"Error while inserting posts: {e}")

if __name__ == "__main__":
    inserter = WeaviatePostInserter()
    inserter.process_and_insert_posts()
