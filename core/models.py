import os
import shutil
from hashlib import md5

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.db import models

from SecurAPK import settings


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


def hash_upload(instance, filename):
    instance.file.open()
    contents = instance.file.read()
    apk_hash = md5(contents).hexdigest()
    apk_path = os.path.join(settings.MEDIA_ROOT, apk_hash)
    if os.path.exists(apk_path):
        shutil.rmtree(apk_path)
    return os.path.join(apk_hash,'apk.apk')


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    if not ext.lower() == '.apk':
        raise ValidationError(u'Unsupported file extension.')


class App(BaseModel):
    file = models.FileField(upload_to=hash_upload, validators=[validate_file_extension])
    name = models.CharField(max_length=30)
    ready = models.BooleanField(default=False)
