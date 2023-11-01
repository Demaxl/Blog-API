from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

"""
/articles/1/like

"""

router = DefaultRouter(trailing_slash=False)
router.register("articles", views.ArticleViewSet, basename="articles")

urlpatterns = [
    path("", include(router.urls)),
    path("author/<slug:username>", views.AuthorView.as_view()),
    path("author/me/liked-articles", views.AuthorLikesView.as_view())
]
