import utils.classes as class_manager
"""
Read existing classes and their statuses from the Docker volume under the path /class_data/status.json.
The file is formatted as follows:
{
    "classes": [
        {
            "name": "CS 103",
            "url": "https://piazza.com/class/...",
            "status": "ready"
        },
        {
            "name": "CS 104",
            "url": "https://piazza.com/class/...",
            "status": "scraped"
        },
    ]
}
The CLI is responsible for receiving the user prompt on whether a new class is to be added or an existing class is to be chat with/deleted.
"""

def print_classes(classes):
    """This function prints the classes."""
    if classes == None or len(classes) == 0:
        print("No classes found.")
    else:
        print("Your current classes:")
        for i, class_ in enumerate(classes):
            print(f"{i+1}. {class_['name']} ({class_['url']}) - {class_['status']}")

def start_cli():
    """This function starts the CLI."""
    # Load the classes from the Docker volume
    classes = class_manager.load_classes()

    # Print the classes
    print_classes(classes)

    choice = 0
    while choice < 1 or choice > 4:
        # Prompt the user for input
        print("What would you like to do?")
        print("1. Add new class")
        print("2. Chat with existing class")
        print("3. Delete existing class")
        print("4. Exit")
        choice = int(input("Enter your choice: "))

        # Validate user input
        if choice not in [1, 2, 3, 4]:
            print("Invalid choice. Please try again.")
        
    
    # Handle add new class
    if choice == 1:
        # Prompt the user for input
        class_name = input("Enter the name of the class: ")
        class_url = input("Enter the URL of the class: ")
        user_role = input("What is your role in the class? (instructor/student): ")

        # Add the class
        class_manager.add_class(class_name=class_name, class_url=class_url, user_role=user_role)
        print("Class added successfully.")
        
        # Start reading the class. We have the reader class for this. This is a 
        from reader.class_reader import ClassReader
        print("Configuring the reader to collect Piazza posts...")
        class_reader = ClassReader()
        class_reader.prepare_config(class_path=class_url, role=user_role)
        print("Configuration completed successfully. Reading posts...")
        class_reader.read_class()

        # Get the file paths used by the reader
        read_file_paths = class_reader.file_paths

        # Add the class to the vector database
        print("Adding posts to the vector database...")


    # Handle exit
    if choice == 4:
        print("Exiting. Goodbye!")
        return