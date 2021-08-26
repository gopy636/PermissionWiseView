
from app1.models import *
from rest_framework import serializers



class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model= AppUser
        fields = ('first_name','last_name','is_admin','date_of_birth','photo_url','email')


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(max_length=50, required=True)

class AppUserSerializerAdmin(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField("full_name1")

    class Meta:
        model= AppUser
        fields = ('id','full_name','first_name','last_name','email')


    def full_name1(self, obj):

        if obj.first_name:
            full_name = obj.first_name + obj.last_name
        else:
            full_name = None
        return full_name

