import weaviate
import weaviate.classes as wvc
from weaviate.util import generate_uuid5

import os
import re

class_name = "PiazzaPosts"
collection = None

# Create the local client
client = weaviate.connect_to_local(
    port=8080,
    grpc_port=50051,
    headers={"X-OpenAI-Api": os.getenv("OPENAI_API_KEY")}
)


def extract_number(filename):
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else 0


def process_posts():
    total = 0
    posts = []
    post_data = {}
    for filename in sorted(os.listdir('posts'), key=extract_number):
        with open(os.path.join('posts', filename), 'r') as file:
            file_content = file.read()
            if "metadata" in filename:
                post_data['metadata'] = file_content
            else:
                post_data['content'] = file_content
            if 'metadata' in post_data and 'content' in post_data:
                properties = {"metadata": post_data['metadata'], "content": post_data['content']}
                post_object = wvc.DataObject(
                    properties=properties,
                    uuid=generate_uuid5(properties)
                )
                posts.append(post_object)
                post_data.clear()
                total += 1
    print("Total entries:", total)
    return posts  # Return the list of posts for further processing


def insert_posts_to_db(posts):
    global collection
    response = collection.data.insert_many(posts) # Will insert without a batch, according to the docs
    print(response)


def search(query_text):
    global collection
    try:
        response = collection.query.near_text(
            query=query_text,
            limit=8,
            return_metadata=wvc.query.MetadataQuery(distance=True)
        )
        return response
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def run_search_loop():
    while True:
        user_input = input("Enter your query (type 'exit' or 'quit' to end): ")

        if user_input.lower() in ['exit', 'quit']:
            print("Exiting program.")
            break

        response = search(user_input)
        if response:
            print("Query response:", response)


def create_collection():
    global collection
    client.collections.create(
        name=class_name,
        vectorizer_config=wvc.Configure.Vectorizer.text2vec_openai(),
        generative_config=wvc.Configure.Generative.openai(),
        properties=[
            wvc.Property(name="metadata", data_type=wvc.DataType.TEXT),
            wvc.Property(name="content", data_type=wvc.DataType.TEXT),
        ]
    )
    collection = client.collections.get(class_name)


def setup_db():
    create_collection()
    posts_to_insert = process_posts()
    insert_posts_to_db(posts_to_insert)


def run_db():
    try:
        collection = client.collections.get(class_name)
        print("Collection found in Docker volume. Starting...")
    except Exception as e:
        # Create the collection if it doesn't exist. No other error is expected.
        print("Collection not found in Docker volume. Creating and inserting posts...")
        setup_db()


