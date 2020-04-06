from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Files(models.Model):
    fileid = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    files = models.FileField(upload_to='files/')
    create_dte = models.DateTimeField(default=datetime.now)