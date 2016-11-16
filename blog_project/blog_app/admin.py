from django.contrib import admin
from .models import User, Ad, Category, Tag, Article, Comment, Links
# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
	list_display = ('title', 'desc', 'content')
	class Media:
		js = (
			'js/editor/kindeditor-4.1.10/kindeditor-all.js',
			'js/editor/kindeditor-4.1.10/config.js',
			'js/editor/kindeditor-4.1.10/lang.zh_CN.js',
		)
admin.site.register(User)
admin.site.register(Ad)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
admin.site.register(Links)
