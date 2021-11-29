from typing import Text
from django.db import models

from django.db.models import Model

from django.contrib.auth.models import User
from django.db.models.fields import CharField, TextField, IntegerField
from django.db.models.fields.related import ForeignKey

# Create your models here.

# Post Model
class Post(Model):
    title = CharField(max_length=100)
    image = CharField(max_length=500)
    description = TextField(max_length=5000)
    # locationName = CharField(max_length=100)
    lat = CharField(max_length=9)
    long = CharField(max_length=9)

    user = ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

    def __str__(self):
        return self.title