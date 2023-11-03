from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from .serializers import ArticleSerializer, ProfileSerializer, CommentSerializer
from .models import Article, Comment, Reply, Profile
from .permissions import IsAuthorOrReadOnly, IsCommenterOrReadOnly


class AuthorView(generics.RetrieveAPIView):
    queryset = Profile.objects.select_related("user")
    serializer_class = ProfileSerializer
    lookup_field = "user__username"
    lookup_url_kwarg = "username"

class AuthorLikesView(generics.ListAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.liked_articles.all()
    

class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthorOrReadOnly]

    search_fields = ["title"]
    ordering_fields = ["time_posted"]


    def get_queryset(self):
        queryset = Article.objects.select_related("author")
        author = self.request.query_params.get("author")

        if author:
            queryset = queryset.filter(author__username=author)

        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def me(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(author=request.user)
        
        serialized_items = ArticleSerializer(queryset, many=True)
        return Response(serialized_items.data)
    
    @action(detail=True, methods=["POST"], permission_classes=[IsAuthenticated])
    def like(self, request, *args, **kwargs):
        article = self.get_object()

        msg = article.like(request.user)
        return Response({"success":True, "Message":msg})
     

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsCommenterOrReadOnly]

    def get_queryset(self):
        queryset = Comment.objects.filter(article_id=self.kwargs['article_pk'])
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user, article_id=self.kwargs['article_pk'])

    @action(detail=True, methods=["POST"], permission_classes=[IsAuthenticated])
    def like(self, request, *args, **kwargs):
        comment = self.get_object()

        msg = comment.like(request.user)
        return Response({"success":True, "Message":msg})

    
