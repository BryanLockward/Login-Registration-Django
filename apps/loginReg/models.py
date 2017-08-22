# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import bcrypt
from django.db import models

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')


class UserManager(models.Manager):
    def validate_login(self, check_user):
        errors = ""
        if len(self.filter(email=check_user['email'])) > 0:
            user = self.filter(email=check_user['email'])[0]
            if not bcrypt.checkpw(check_user['password'].encode(), user.password.encode()):
                errors="Incorrect Password"
        else:
            errors="Incorrect Email"

        return errors

    def validate_registration(self,user):
        errors=[]

        if len(user['first_name']) < 2:
            errors.append("First Name must have more than two characters")
        if len(user['last_name'])<2:
            errors.append("Last Name must have more than two characters")
        if len(user['password']) < 8:
            errors.append("password must be at least 8 characters")
        if not re.match(EMAIL_REGEX, user['email']):
            errors.append("Invalid email")
        if len(User.objects.filter(email=user['email'])) > 0:
            errors.append("email already in use")
        if user['password'] != user['password_confirm']:
            errors.append("passwords do not match")

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    objects = UserManager()
    def __str__(self):
        return self.email
