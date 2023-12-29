import weaviate
import weaviate.classes as wvc
import os
import re


client = weaviate.Client(
    url = "http://localhost:8080",
    additional_headers = {
        "X-OpenAI-Api-Key": os.environ.get("OPENAI_API_KEY")  # Replace with your inference API key
    }
)

# client.schema.delete_class("CSCI350")

class_data = client.schema.create_class({
    "class": "CSCI350",
    "vectorizer": "text2vec-openai",  # If set to "none" you must always provide vectors yourself. Could be any other "text2vec-*" also.
    "moduleConfig": {
        "text2vec-openai": {},
        "generative-openai": {}  # Ensure the `generative-openai` module is used for generative queries
    },
    "properties": [
        {
            "name": "metadata",
            "dataType": ["text"],
        },
        {
            "name": "content",
            "dataType": ["text"],
        },
    ],
})

def extract_number(filename):
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else 0


def process_posts():
    total = 0
    post_data = list()
    # open posts files in alphabetical order
    for filename in sorted(os.listdir('posts'), key=extract_number):
        with open(os.path.join('posts', filename), 'r') as file:
            file_content = file.read()  # Read the file once as a string
            if "metadata" in filename:
                post_data.insert(0, file_content)  # Insert metadata at the beginning of the list
            else:
                post_data.insert(1, file_content)
  
        if len(post_data) == 2:
            total += 1
            insert_post_to_db(post_data[0], post_data[1])
            post_data = list()

    print("Total entries:", total)

def insert_post_to_db(metadata, content):
    client.batch.add_data_object(
        data_object={"content": content, "metadata": metadata},
        class_name="CSCI350"
    )

process_posts()
