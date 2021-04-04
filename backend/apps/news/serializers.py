from rest_framework import serializers
from apps.media.models import Media
from .models import News

class StoriesCreateSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    image = serializers.ListField(child = serializers.ImageField(required = False),required=False )  
  

class ImageUrlField_Get(serializers.RelatedField):
    def to_representation(self, instance):
        url = instance.image.url
        pk = instance.pk
        request = self.context.get('request', None)
        if request is not None:
            return request.build_absolute_uri(url)
        return ({'pk': pk, 'url': url})

class ImageUrlField(serializers.RelatedField):
    def to_representation(self, instance):
        url = instance.image.url
        request = self.context.get('request', None)
        if request is not None:
            return request.build_absolute_uri(url)
        return url

class ListImageSerializer(serializers.ModelSerializer):
    image = serializers.ListField(child = serializers.ImageField(required = False, allow_null=True) )  
    class Meta:
        model = Media
        fields = ['image']   

class StoriesUniqueSerializer(serializers.ModelSerializer):
    image=ImageUrlField_Get(read_only=True, many= True, required= False)
    user = serializers.SerializerMethodField("get_user")
    class Meta:
        model = News
        fields =["pk","title","description","likes","image","created_at","user"]

    def get_user(self, obj):
        data = {
            "username":obj.user.username,
            "email": obj.user.email,
            "photo": obj.user.image
        }
        return data

class StoriesWebSerializer(serializers.ModelSerializer):
    image=ImageUrlField(read_only=True, many= True)
    user = serializers.SerializerMethodField("get_user")
    class Meta:
        model = News
        fields =["pk","title","description","likes","image","created_at","user"]

    def get_user(self, obj):
        data = {
            "username":obj.user.username,
            "email": obj.user.email,
            "photo": obj.user.image
        }
        return data
