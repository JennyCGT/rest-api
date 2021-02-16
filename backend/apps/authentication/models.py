from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from .manager import UserManager
from apps.media.models import Media
from timestampedmodel import TimestampedModel


class GenderChoice(models.TextChoices):
    MALE = u'M', 'Male'
    FEMALE = u'F', 'Female'
    OTHERS = u'O', 'Other'


class User(AbstractUser, TimestampedModel):
    first_name = models.CharField(max_length=50,blank=True)
    last_name = models.CharField(max_length=50,blank=True)
    username = None # remove username field, we will use email as unique identifier
    email = models.EmailField(unique=True, null=True, db_index=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    gender = models.CharField(max_length=2,choices=GenderChoice.choices,blank=True,null=True)
    identity_card = models.CharField(unique=True,null=True,max_length=11,blank=True)
    birthdate = models.DateField(null=True,blank=True)
    image = models.OneToOneField(Media, on_delete=models.CASCADE, related_name='media', null=True,blank=True)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    objects = UserManager()