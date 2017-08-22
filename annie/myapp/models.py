# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from uuid import uuid4

# Create your models here.
from django.db import models
class User(models.Model):
    email = models.EmailField(default=False)
    name = models.CharField(max_length=120,default=False)
    username = models.CharField(max_length=120,default=False)
    password = models.CharField(max_length=40,default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


class SessionToken(models.Model):
    user = models.ForeignKey(User)
    session_token = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=True)

    def create_token(self):
        self.session_token=str(uuid4())

class PostModel(models.Model):
  user = models.ForeignKey(User)
  image = models.FileField(upload_to='user_images')
  image_url = models.CharField(max_length=255)
  caption = models.CharField(max_length=240)
  created_on = models.DateTimeField(auto_now_add=True)
  updated_on = models.DateTimeField(auto_now=True)

class LikeModel(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey(PostModel)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)








