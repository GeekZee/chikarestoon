from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import User as AppUser
# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=80, unique=True)

    def __str__(self) -> str:
        return f"{self.category_name}"


class UserInfo(models.Model):
    bio = models.TextField(max_length=500, null=True, blank=True)
    profile = models.ImageField(null=True, blank=True)
    user_auth = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user_auth.username}"


class Ideas(models.Model):
    title = models.CharField(max_length=80)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    category_ides = models.OneToOneField(Category, null=True, on_delete=models.SET_NULL)
    idea_writer = models.ForeignKey(AppUser, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.idea_writer.username} : {self.title}"


class Stars(models.Model):
    star_number = models.IntegerField()
    star_idea = models.ForeignKey(Ideas, on_delete=models.CASCADE)
    star_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.star_user.username} : {self.star_idea.title} : {self.star_number}"
