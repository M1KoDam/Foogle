import os
import sys


class FilesFinder:
    def __init__(self, path=r'C:\Users', ignore=None, permissions=None):
        self.path = path
        self.files = []
        self.catalogs = []

        if ignore is None:
            self.get_system_directories()
        else:
            self.ignore_catalog = ignore

        if permissions is None:
            self.permissions = ["txt"]
        else:
            self.permissions = permissions

    def get_system_directories(self):
        if sys.platform.startswith('win'):
            self.ignore_catalog = ['Windows']
        elif sys.platform.startswith('linux'):
            self.ignore_catalog = ['mnt', 'proc', 'sys']

    def get_files_directory(self):
        for root, dirs, files in os.walk(self.path):
            for file_name in files:
                prepend_files = os.path.join(root, file_name)
                for permission in self.permissions:
                    if prepend_files.endswith(permission):
                        self.files.append(prepend_files)
            for dir_name in dirs:
                prepend_directory = os.path.join(root, dir_name)
                if not any(ignore in prepend_directory for ignore in self.ignore_catalog):
                    self.catalogs.append(prepend_directory)
        return self.files


v = FilesFinder()
print(v.get_files_directory())
