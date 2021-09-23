from django.db import models

# Create your models here.
class UserInfo(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(max_length=500, null=True, blank=True)
    profile = models.ImageField(null=True, blank=True)
    user_ideas = models.ForeignKey('Ideas', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.name}"


class Ideas(models.Model):
    title = models.CharField(max_length=80)
    text = models.TextField()
    stars = models.IntegerField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    writer = models.OneToOneField(
        UserInfo,
        max_length=100,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __str__(self) -> str:
        return f"{self.writer.name} : {self.title}"