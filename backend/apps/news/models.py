from django.db import models
from django.db.models.deletion import CASCADE
from timestampedmodel import TimestampedModel
from apps.authentication.models import User
from apps.media.models import Media

class News(TimestampedModel,models.Model):
    title= models.CharField(max_length=500, null= True,blank=True)
    description = models.TextField(null=True,blank= True)
    image = models.ManyToManyField(Media, related_name='stories_image')
    likes = models.IntegerField(null=True, blank=True,default=0)
    user = models.ForeignKey(User, on_delete= CASCADE, blank= True, null= True)
