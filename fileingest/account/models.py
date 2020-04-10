from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Files(models.Model):
    uploadid = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    files = models.FileField(upload_to='files/')
    create_dte = models.DateTimeField(default=datetime.now)
	
class FileLogs(models.Model):
	uploadid = models.ForeignKey(Files, null=False, on_delete=models.CASCADE, related_name='upload_id')
	files = models.CharField(max_length=250, null=False)
	logs = models.CharField(max_length=250, default="TEST")
	create_dte = models.DateTimeField(default=datetime.now)