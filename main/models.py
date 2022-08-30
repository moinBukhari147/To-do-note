from email.policy import default
from msilib import sequence
from statistics import mode
from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

# Create your models here.

class profile(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    profile_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user_seq = models.IntegerField(default=0)
    fname = models.CharField(max_length=30, default='no name')
    lname = models.CharField(max_length=30, default='no name')
    username = models.CharField(max_length=30)
    profile_img = models.ImageField(upload_to='dp', default = 'dp/blank-profile-picture.webp')
    def __str__(self):
        return self.username
class note(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=None)
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, default='no title')
    date_time = models.DateTimeField(default=datetime.now())
    note_content = models.CharField(max_length=500, default='no Content')
    def __str__(self) -> str:
        return self.title

