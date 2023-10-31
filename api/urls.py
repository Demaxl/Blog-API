from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

"""
/articles?author=demaxl

"""

router = DefaultRouter(trailing_slash=False)
router.register("articles", views.ArticleViewSet, basename="articles")

urlpatterns = [
    path("", include(router.urls)),
    path("author/<slug:username>", views.AuthorView.as_view())
]
