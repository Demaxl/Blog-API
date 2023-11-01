from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from .serializers import ArticleSerializer, ProfileSerializer
from .models import Article, Comment, Reply, Profile
from .permissions import IsAuthorOrReadOnly


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
     
   