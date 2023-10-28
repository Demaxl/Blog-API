from django.db import models
from django.contrib.auth.models import User, AnonymousUser
from django.core.validators import MinValueValidator

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", primary_key=True)
    date_joined = models.DateField(auto_now_add=True)
    bio = models.TextField(max_length=500)
    image = models.URLField()

class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articles")
    title = models.CharField(max_length=255)
    body = models.TextField(max_length=5000)
    time_posted = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked_articles")

class BaseComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(max_length=300)
    likes = models.IntegerField(validators=[MinValueValidator(0)])

    class Meta:
        abstract = True

class Comment(BaseComment):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")

class Reply(BaseComment):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="replies")