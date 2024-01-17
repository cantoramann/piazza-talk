def load_existing_classes(file_path='classes.txt'):
    with open(file_path, 'r') as file:
        classes = file.read().strip().split(',')
        return classes
