from django.urls import path, include
from rest_framework_nested import routers
from . import views

"""
/articles/1/comments/1/replies

"""

article_router = routers.DefaultRouter(trailing_slash=False)
article_router.register("articles", views.ArticleViewSet, basename="articles")

comments_router = routers.NestedDefaultRouter(article_router, "articles", lookup="article")
comments_router.register("comments", views.CommentViewSet, basename="article-comments")


urlpatterns = [
    path("", include(article_router.urls)),
    path("", include(comments_router.urls)),
    path("author/<slug:username>", views.AuthorView.as_view()),
    path("author/me/liked-articles", views.AuthorLikesView.as_view())
]
