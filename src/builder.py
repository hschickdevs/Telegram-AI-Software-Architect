import os

class CodebaseBuilder:
    def __init__(self, project_folder):
        self.project_folder = project_folder

    def create_directories(self, path):
        os.makedirs(path, exist_ok=True)

    def create_file(self, path, content):
        with open(path, 'w') as file:
            file.write(content)

    def build_codebase(self, response):
        # Create project folder
        self.create_directories(self.project_folder)

        # Iterate over the files in the response
        for filepath, content in response['files'].items():
            # Create directories if they don't exist
            directory = os.path.dirname(filepath)
            if directory:
                self.create_directories(os.path.join(self.project_folder, directory))
            
            # Create the file and write the content
            self.create_file(os.path.join(self.project_folder, filepath), content)

        print("Project created successfully!")
        
    def clean_up(self):
        if os.path.exists(self.project_folder):
            shutil.rmtree(self.project_folder)