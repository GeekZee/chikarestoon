from django.contrib import admin
from .models import Ideas, UserInfo, Stars, Category
# Register your models here.
admin.site.register(Ideas)
admin.site.register(UserInfo)
admin.site.register(Stars)
admin.site.register(Category)
