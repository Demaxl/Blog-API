from django.db import models
from django.contrib.auth.models import User, AnonymousUser
from django.core.validators import MinValueValidator
from itertools import chain
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


DEFAULT_IMG_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Windows_10_Default_Profile_Picture.svg/2048px-Windows_10_Default_Profile_Picture.svg.png"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", primary_key=True)
    bio = models.TextField(max_length=500, blank=True)
    image = models.URLField(default=DEFAULT_IMG_URL)

    def __str__(self) -> str:
        return f"{self.user}'s profile"

class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articles")
    title = models.CharField(max_length=255)
    body = models.TextField(max_length=5000)
    time_posted = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked_articles", blank=True)

    def __str__(self):
        return f"{self.title}"

    def like(self, user):
        if self.likes.contains(user):
            return
        self.likes.add(user)
        


class BaseComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(max_length=300)
    time_posted = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.user}: {self.body[:20]}..."

    def like(self, user):
        if self.likes.contains(user):
            return
        self.likes.add(user)
        
    

class Comment(BaseComment):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")
    likes = models.ManyToManyField(User, blank=True, related_name="liked_comments")


class Reply(BaseComment):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="replies")
    likes = models.ManyToManyField(User, blank=True, related_name="liked_replies")

