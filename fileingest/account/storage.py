from django.core.files.storage import FileSystemStorage
from django.utils.deconstruct import deconstructible
import os
from django.conf import settings 

@deconstructible
class CustomFileSystemStorage(FileSystemStorage):

    def get_valid_name(self, name):
        return name

    def get_available_name(self, name, max_length=None):
        if self.exists(name):
           os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name 