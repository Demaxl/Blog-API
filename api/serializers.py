from rest_framework import serializers

from django.contrib.auth.models import User
from .models import Article, Comment, Reply, Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'date_joined')
        read_only_fields = ('first_name', 'last_name', 'date_joined')

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.SlugRelatedField(slug_field="username", source="user", read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    date_joined = serializers.DateTimeField(source='user.date_joined', read_only=True)

    class Meta:
        model = Profile
        fields = ('username', 'first_name', 'last_name',"email", 'date_joined', 'bio', 'image')
        read_only_fields = ('username', 'first_name', 'last_name', 'date_joined', 'bio', 'image')




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
    
class CommentSerializer(serializers.ModelSerializer):
    comment_id = serializers.IntegerField(source="id", read_only=True)
    user = serializers.SlugRelatedField(slug_field="username", read_only=True)

    likes_count= serializers.SerializerMethodField("getLikes")
    replies_count = serializers.SerializerMethodField("getRepliesCount")


    class Meta:
        model = Comment
        fields = ["article_id", "comment_id", "user", "body", "time_posted", "likes_count", "replies_count"]

    def getLikes(self, comment: Comment):
        return comment.likes.count()

    def getRepliesCount(self, comment: Comment):
        return comment.replies.count()