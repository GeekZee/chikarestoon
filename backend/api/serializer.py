from rest_framework import serializers
from .models import Ideas, Stars, UserInfo, Category

# from drf_dynamic_fields import DynamicFieldsMixin


class IdeasSerializers(serializers.ModelSerializer):

    def get_author(self, obj):
        return {
            "username": obj.idea_writer.username,
            "first_name": obj.idea_writer.first_name,
            "last_name": obj.idea_writer.last_name,
        }

    author = serializers.SerializerMethodField("get_author")

    class Meta:
        model = Ideas

        # select all fields:
        fields = '__all__'


