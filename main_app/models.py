# from typing import Text
from django.db import models

from django.db.models import Model

from django.contrib.auth.models import AbstractUser
from django.db.models.fields import CharField, DateTimeField, TextField
from django.db.models.fields.related import ForeignKey

# Create your models here.

# User Model
class User(AbstractUser):
    location = CharField(max_length=70)
    # image = CharField(max_length=500) // omitting image for now

    def __str__(self):
        return self.username

# Post Model
class Post(Model):
    title = CharField(max_length=100)
    image = CharField(max_length=500)
    description = TextField(max_length=5000)
    lat = CharField(max_length=10)
    # Longitude is 1 extra because they can go into triple digits
    long = CharField(max_length=11)

    image_time = DateTimeField(blank=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    user = ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

    def __str__(self):
        return self.title