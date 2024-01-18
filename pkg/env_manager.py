"""
Functional interface to load and save environment variables.
The environment variables file is mounted inside the Docker volume.
Hence, the program is not using an environment variable file.
Environment variables are stored in a json file named env.json.
"""
import json
import os

env_file = "/class_data/env.json"  # Adjust the path as needed

def load_all_envs():
    """ Load all environment variables from the JSON file. """
    if os.path.exists(env_file):
        with open(env_file, 'r') as file:
            return json.load(file)
    return {}

def load_env(key):
    """ Load a specific environment variable by key. """
    envs = load_all_envs()
    return envs.get(key)

def save_env(key, value):
    """ Save an environment variable to the JSON file. """
    envs = load_all_envs()
    envs[key] = value
    with open(env_file, 'w') as file:
        json.dump(envs, file, indent=4)