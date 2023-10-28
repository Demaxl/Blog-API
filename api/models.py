from django.db import models
from django.contrib.auth.models import User, AnonymousUser
from django.core.validators import MinValueValidator

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
    likes = models.ManyToManyField(User, related_name="liked_articles")

    def __str__(self):
        return f"{self.title}"

class BaseComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(max_length=300)
    likes = models.IntegerField(validators=[MinValueValidator(0)])

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.user}: {self.body[:20]}..."

class Comment(BaseComment):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")

class Reply(BaseComment):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="replies")