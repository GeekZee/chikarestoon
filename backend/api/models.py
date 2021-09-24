from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)

    def __str__(self) -> str:
        return f"{self.name}"


class UserInfo(models.Model):
    bio = models.TextField(max_length=500, null=True, blank=True)
    profile = models.ImageField(null=True, blank=True)
    user_auth = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user_auth.username}"


class Ideas(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField(max_length=3000)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, null=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.author.username} : {self.title}"


class Stars(models.Model):
    star_idea = models.ForeignKey(Ideas, on_delete=models.CASCADE)
    star_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.star_user.username} : {self.star_idea.title} : {self.star_number}"
