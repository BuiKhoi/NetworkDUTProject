import os
from shutil import rmtree

class LocalHandler:
    def __init__(self, start_folder='/'):
        self.start_folder = start_folder
        self.current_folder = start_folder
        
    def get_current_folder(self):
        return self.current_folder
    
    def open_folder(self, folder):
        self.current_folder += folder + '/'
        return self.current_folder

    def back_folder(self):
        idx = self.current_folder[:-1].rfind('/')
        self.current_folder = self.current_folder[:idx+1]
    
    def create_folder(self, folder_name):
        os.mkdir(self.current_folder + folder_name)
        
    def delete_folder(self, folder_name):
        rmtree(self.current_folder + folder_name)
        
    def delelte_file(self, file_name):
        os.remove(self.current_folder + file_name)
        
    def get_folder_items(self):
        return os.listdir(self.current_folder)

    def check_root(self):
        return self.current_folder == self.start_folder