# encoding: utf-8
from django.shortcuts import render
import logging
from django.conf import settings
from models import Category, Article, Comment
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger

import sys  
reload(sys)  
sys.setdefaultencoding('utf8')


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

	comment_list = Comment.objects.all()

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


	#文章归档
	#以月份去重
	#原生sql

	#article_date = Article.objects.raw("select id, DATE_FORMAT(date_publish, '%%Y-%%m') as date from blog_app_article")
	#for date in article_date:
	#	print(date)

	#from django.db import connection
	#cursor = connection.cursor()
	#cursor.execute('select distinct DATE_FORMAT(date_publish, "%Y年%m月") as date from blog_app_article')	
	#date = cursor.fetchall()	
	#date_utf8 = []

	distinct_date_list = Article.objects.distinct_date()

	#for d in date:
	#	date_utf8.append(d[0].decode('utf8'))	
	return render(request, 'index.html', locals())

def archive(request):
	if request.GET.get('date'):
		date = request.GET.get('date')
		year = date[:4]	
		month = date[5:7]
	else:
		year = request.GET.get('year')
		month = request.GET.get('month')

	page_data = 2
	category_list = Category.objects.all()	


	comment_list = Comment.objects.all()

	try:
		page = int(request.GET.get('page','1'))
		page_all = int(request.GET.get('page_all', '1'))
		page_type = request.GET.get('page_type')
	except ValueError:
		page = 1
		page_all =1
	if page == 1 and page_all == 1:
		page_all = Article.objects.filter(date_publish__icontains=year+'-'+month).count()/page_data
		print(page_all)
		if Article.objects.filter(date_publish__icontains=year+'-'+month).count()%page_data > 0:
			page_all = page_all+1
	if page_type=='up':
		page = page-1
	if page_type=='down':
		page = page+1
	page_start = (page-1)*page_data
	if page == page_all:
		page_end = Article.objects.filter(date_publish__icontains=year+'-'+month).count()
	else:
		page_end = page*page_data

	article_list = Article.objects.filter(date_publish__icontains=year+'-'+month)[page_start:page_end]	

	distinct_date_list = Article.objects.distinct_date()


	return render(request, 'archive.html', locals())
	
