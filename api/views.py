from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework import exceptions
from functools import wraps

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


class BaseCommentViewSet(viewsets.ModelViewSet) :
    permission_classes = [IsCommenterOrReadOnly]

    def dispatch(self, request, *args, **kwargs):
        article_id = kwargs.get('article_pk')
        comment_id = kwargs.get("comment_pk")

        if article_id and not article_id.isdigit():
            kwargs.update({"article_pk":-1})

        if comment_id and not comment_id.isdigit:
            kwargs.update({"comment_pk":-1})

        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self, parent, model, pk):
        parent_model = get_object_or_404(parent, pk=pk)
        queryset = model.objects.filter(**{parent.__name__.lower():parent_model})
        return queryset
    
    def perform_create(self, serializer, parent, pk):
        parent_model = get_object_or_404(parent, pk=pk)
        serializer.save(user=self.request.user, **{parent.__name__.lower():parent_model})

    

class CommentViewSet(BaseCommentViewSet):
    serializer_class = CommentSerializer
   

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(
            Article, Comment, self.kwargs['article_pk']
            )
    
    def perform_create(self, serializer, *args, **kwargs):
        return super().perform_create(
            serializer, Article, self.kwargs['article_pk']
        )
    
    @action(detail=True, methods=["POST"], permission_classes=[IsAuthenticated])
    def like(self, request, *args, **kwargs):
        instance = self.get_object()

        msg = instance.like(request.user)
        return Response({"success":True, "Message":msg})

    
