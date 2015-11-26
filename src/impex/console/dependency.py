from os import fwalk
from os.path import getmtime
from os.path import join

from baelfire.dependencies import Dependency


class MigrationChanged(Dependency):

    def __init__(self, src_name, destination_name):
        super().__init__()
        self.src_name = src_name
        self.destination_name = destination_name

    @property
    def src(self):
        return self.paths[self.src_name]

    @property
    def destination(self):
        return self.paths[self.destination_name]

    def should_build(self):
        try:
            destination_time = getmtime(self.destination)
        except FileNotFoundError:
            return True
        for root, dirs, files, rootfd in fwalk(self.src):
            for filename in files:
                file_path = join(root, filename)
                if destination_time < getmtime(file_path):
                    return True
        return False
