# cirkut/dropbox_storage.py
from storages.backends.dropbox import DropBoxStorage
import posixpath

class FixedDropBoxStorage(DropBoxStorage):
    def _full_path(self, name):
        # শুধু filename নাও, Windows path বাদ দাও
        name = posixpath.basename(name.replace("\\", "/"))
        if self.root_path:
            return posixpath.join(self.root_path, name)
        return "/" + name