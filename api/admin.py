from django.contrib import admin
from .models import Article, Comment, Reply, Profile

# Register your models here.
admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(Profile)