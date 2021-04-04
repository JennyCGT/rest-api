from django.db import models
from django.conf import settings
from timestampedmodel import TimestampedModel
# Create your models here.
class Media(TimestampedModel, models.Model   ):
    title = models.CharField(max_length=20,null=True,blank=True)
    description = models.CharField(max_length=200,null=True,blank=True)
    image = models.ImageField(upload_to='image', null=True, max_length=255)
    #image = models.URLField(max_length=200)

    def __str__(self):
        return '{0},{1}'.format(self.pk,self.title,self.image)