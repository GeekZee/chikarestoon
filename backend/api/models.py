from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserInfo(models.Model):
    bio = models.TextField(max_length=500, null=True, blank=True)
    profile = models.ImageField(null=True, blank=True)
    user_ideas = models.ForeignKey('Ideas', on_delete=models.CASCADE, null=True, blank=True)
    user_auth = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user_auth.username}"


class Ideas(models.Model):
    title = models.CharField(max_length=80)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    writer = models.ForeignKey(
        'UserInfo',
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return f"{self.writer.user_auth.username} : {self.title}"


class Stars(models.Model):
    star_number = models.IntegerField()
    star_idea = models.OneToOneField(Ideas, on_delete=models.CASCADE)
    star_user = models.OneToOneField(UserInfo, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.star_user.user_auth.username} : {self.star_idea.title} : {self.star_number}"
