"""
By this time, class data must be read and written to the Docker volume in the path /class_data/{class_url}.
The data is stored in the following format:
 * /class_data/{class_url}/raw/post_{post_id}.txt
 * /class_data/{class_url}/metadata/post_{post_id}_metadata.txt
The loader class is responsible for loading the data from the Docker volume and storing it in the database.
It will read from the config whether to embed the data individually or use the database client's integrated embedding model.
If the user is not using OpenAI embeddings, the embedding model must be called individually for each post.
Finally, if the embedding model is being called individually, regardless of whether the user is using OpenAI embeddings, the embeddings must be stored in the following format:
 * /class_data/{class_url}/embeddings/post_{post_id}_embeddings.txt

For now, only the OpenAI embedding models will be implemented.
"""
import os
import json
import logging
# import config_manager
import env_manager

class DatabaseLoader():
    def __init__(self, class_path, class_name):
        self.logger = logging.getLogger(__name__)
        self.logger.info("Database loader initialized.")
        self.class_path = class_path
        self.class_name = class_name
    

    def setup_loader(self):
        """This function sets up the loader."""
        # embedding_model = config_manager.get('embedding_model')
        embedding_model = 'openai'
        self.embedding_model = embedding_model
        if env_manager.load_env('OPENAI_API_KEY') is None:
            self.logger.error("OpenAI API key not found. Please provide your OpenAI API key on the Environment Variables tab and execute this step after.")
            self.operational = False
        self.operational = True


    def load_class_data():
        pass