from rest_framework import serializers
from .models import Ideas, Stars, UserInfo

from django.contrib.auth import get_user_model
# from drf_dynamic_fields import DynamicFieldsMixin


class IdeasSerializers(serializers.ModelSerializer):

    def get_author(self, obj):
        return {
            "username": obj.idea_writer.username,
            "first_name": obj.idea_writer.first_name,
            "last_name": obj.idea_writer.last_name,
        }

    idea_writer = serializers.SerializerMethodField("get_author")

    class Meta:
        model = Ideas

        # select all fields:
        fields = '__all__'



class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        exclude = ('password', 'email',)
