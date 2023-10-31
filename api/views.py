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
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = "user__username"
    lookup_url_kwarg = "username"

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def me(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(author=request.user)
        
        serialized_items = ArticleSerializer(queryset, many=True)
        return Response(serialized_items.data)
     
   