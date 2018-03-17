# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


# Create your models here.

class AccountUserManager(UserManager):  # inherit from Django's UserManager class

  # override the _create_user method to add a check if email is correct (default uses username for login)
  def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
    '''
    Created and saves a User with the given username, email, and password
    '''
    
    if not email:
      raise ValueError('The given email address must be set')
    if not username:
      raise ValueError('The given username must be set')
    

    email = self.normalize_email(email)
    user = self.model(username=username, email=email,
                      is_staff=is_staff, is_active=True,
                      is_superuser=is_superuser,
                      date_joined=timezone.now(), **extra_fields)
    user.set_password(password)
    user.save(using=self._db)

    return user

  def normalize_email(cls, email):
    """
    Overriding method
    Normalize the address by lowercasing both the name and domain parts
    of the email address.
    """
    email = email or ''
    try:
        email_name, domain_part = email.strip().rsplit('@', 1)
    except ValueError:
        pass
    else:
        email = '@'.join([email_name.lower(), domain_part.lower()])
    return email


class User(AbstractUser): # inherit from Django's AbstractUser class
  # now that we've abstracted this class we can add any
  # number of custom attributes to our user class

  # we can add payment details for example

  # !!! Need to set email validation EmailValidate in django! - find out how !!!
  email = models.EmailField(
    _('email'),
    max_length=150,
    unique=True,
    help_text=_('some help text for email input'),
    # validators=[email_validator],
  )
  objects = AccountUserManager()

  def __str__(self):
    return self.email
