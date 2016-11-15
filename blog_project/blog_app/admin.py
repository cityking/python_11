from django.contrib import admin
from .models import User, Ad, Category, Tag, Article, Comment
# Register your models here.
admin.site.register(User)
admin.site.register(Ad)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Article)
admin.site.register(Comment)
