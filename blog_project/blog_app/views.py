# encoding: utf-8
from django.shortcuts import render
import logging
from django.conf import settings
from models import Category, Article
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger

logger = logging.getLogger('logger_test')

def global_setting(request):
	return {'site_name':settings.SITE_NAME,
		'site_desc':settings.SITE_DESC,
		'sina_site':settings.SINA_SITE,
		'tecent_site':settings.TECENT_SITE,
		'rss_site':settings.RSS_SITE,
		'mail_site':settings.MAIL_SITE,}

# Create your views here.
def index(request):
	page_data = 2
	category_list = Category.objects.all()	

	#日志器的使用
	#logger.debug('this is a debug')

	#文章显示
	#article_list = Article.objects.all()
	try:
		page = int(request.GET.get('page','1'))
		page_all = int(request.GET.get('page_all', '1'))
		page_type = request.GET.get('page_type')
	except ValueError:
		page = 1
		page_all =1
	if page == 1 and page_all == 1:
		page_all = Article.objects.count()/page_data
		if Article.objects.count()%page_data > 0:
			page_all = page_all+1
	if page_type=='up':
		page = page-1
	if page_type=='down':
		page = page+1
	page_start = (page-1)*page_data
	if page == page_all:
		page_end = Article.objects.count()
	else:
		page_end = page*page_data

	article_list = Article.objects.all()[page_start:page_end]	
#	paginator = Paginator(article_list, page_data)
#	try:
#		article_list = paginator.page(page)
#	except(InvalidPage,EmptyPage,PageNotAnInteger):
#		article_list = paginator.page(1)
	return render(request, 'index.html', locals())
