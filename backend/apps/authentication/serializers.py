from rest_framework import serializers
from .models import User


class ImageUrlField(serializers.RelatedField):
    def to_representation(self, instance):
        url = instance.image.url
        request = self.context.get('request', None)
        if request is not None:
            return request.build_absolute_uri(url)
        return url


class UserAuthSerializer(serializers.ModelSerializer):

    image=ImageUrlField(read_only=True)    
    class Meta:
        model = User
        fields = ['pk', 'first_name', 'last_name', 'username','is_active','gender','birthdate','identity_card','image']
        read_only_fields = ['pk','image']


class PasswordSerializer(serializers.Serializer):
    new_password1 = serializers.CharField()
    new_password2 = serializers.CharField()
    old_password = serializers.CharField()


class BulkCreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'first_name', 'last_name', 'email','gender','username',"identity_card","birthdate","image"]
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
            'gender': {'required': False},
            'username': {'required': False},
        }

class UsersSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = [ 'first_name', 'last_name', 'email','username','gender', 'is_active']

