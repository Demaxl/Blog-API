from rest_framework import serializers

from django.contrib.auth.models import User
from .models import Article, Comment, Reply, Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["user", "bio", "image"]



class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True)

    likes_count= serializers.SerializerMethodField("getLikes")
    comment_count = serializers.SerializerMethodField("getCommentCount")

    class Meta:
        model = Article
        fields = ["id", "author", "title", "body", "time_posted", "likes_count", "comment_count"]

    def getLikes(self, article: Article):
        return article.likes.count()
    
    def getCommentCount(self, article: Article):
        return article.comments.count()