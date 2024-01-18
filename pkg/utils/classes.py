import json
import os

file_path = '/class_data/status.json'

# Load the classes from the Docker volume
def load_classes():
    global file_path
    # Check if the file exists
    if not os.path.exists(file_path):
        # If the file does not exist, create it with an empty list
        with open(file_path, 'w') as f:
            json.dump([], f)
    
    with open(file_path, 'r') as f:
        classes = json.load(f)
    return classes

def add_class(class_name, class_url, user_role):
    global file_path
    # Load the classes from the Docker volume
    classes = load_classes()
    # Check if the class already exists
    for class_ in classes:
        if class_['url'] == class_url:
            print("Class already exists.")
            return
    # Add the class
    classes.append({
        'name': class_name,
        'url': class_url,
        'role': user_role,
        'status': 'scraped'
    })
    # Write the classes to the Docker volume
    with open(file_path, 'w') as f:
        json.dump(classes, f)
    print("Class added successfully.")