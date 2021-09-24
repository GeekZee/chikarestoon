from rest_framework import serializers
from .models import Ideas, Stars, UserInfo, Category

# from drf_dynamic_fields import DynamicFieldsMixin


class IdeasSerializers(serializers.ModelSerializer):

    def get_author(self, obj):
        return {
            "username": obj.author.username,
            "first_name": obj.author.first_name,
            "last_name": obj.author.last_name,
        }

    author = serializers.SerializerMethodField("get_author")

    class Meta:
        model = Ideas

        # select all fields:
        fields = '__all__'


