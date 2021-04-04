from rest_framework import serializers
from .models import Media

class MediaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Media
        fields = ['title','description','image']
        extra_kwargs = {'image': {'required': True}}

class MediaGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['image']
