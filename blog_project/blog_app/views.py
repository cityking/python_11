# encoding: utf-8
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect 
import logging
from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from forms import Comment_form, Reg_Form, Login_Form
from django.contrib.auth.hashers import make_password
from models import Category, Article, Comment, User
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger
from django.db.models import Count


import sys  
reload(sys)  
sys.setdefaultencoding('utf8')


logger = logging.getLogger('logger_test')

def global_setting(request):
	try:
		site_name=settings.SITE_NAME
		site_desc=settings.SITE_DESC
		sina_site=settings.SINA_SITE
		tecent_site=settings.TECENT_SITE
		rss_site=settings.RSS_SITE
		mail_site=settings.MAIL_SITE
		site_url = settings.SITE_URL
		category_list = Category.objects.all()
		comment_list = Comment.objects.all()
		#评论排行
		comment_article_list = Comment.objects.values('article').annotate(comment_count=Count('article')).order_by('-comment_count')
		article_comment_list = [Article.objects.get(pk = comment['article']) for comment in comment_article_list]
	except Exception as e:
		logger.error(e)
	return locals() 

def getPage(request, article_count, article_all, page_data, page, page_all, page_type):
	try:
		page_start = (page-1)*page_data
		if page == page_all:
		        page_end = article_count 
		else:
		        page_end = page*page_data
		
		article_list = article_all[page_start:page_end]
		return article_list
	except Exception as e:
		logger.error(e)
# Create your views here.
def index(request):
	try:
		page_data = 2
        	try:
        	        page = int(request.GET.get('page','1'))
        	        page_all = int(request.GET.get('page_all', '1'))
        	        page_type = request.GET.get('page_type')
        	except ValueError:
        	        page = 1
        	        page_all =1

		article_count = Article.objects.count()
        	if page == 1 and page_all == 1:
        	        page_all = article_count/page_data
        	        if article_count%page_data > 0:
        	                page_all = page_all+1
        	if page_type=='up':
        	        page = page-1
        	if page_type=='down':
        	        page = page+1


		#日志器的使用
		#logger.debug('this is a debug')


		#文章显示
		#article_list = Article.objects.all()
		article_all = Article.objects.all()
		article_list = getPage(request, article_count, article_all, page_data, page, page_all, page_type)

#		paginator = Paginator(article_list, page_data)
#		try:
#			article_list = paginator.page(page)
#		except(InvalidPage,EmptyPage,PageNotAnInteger):
#			article_list = paginator.page(1)


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
	except Exception as e:
		logger.error(e)
	return render(request, 'index.html', locals())

def archive(request):
	try:
		if request.GET.get('date'):
			date = request.GET.get('date')
			year = date[:4]	
			month = date[5:7]
		else:
			year = request.GET.get('year')
			month = request.GET.get('month')

        	try:
        	        page = int(request.GET.get('page','1'))
        	        page_all = int(request.GET.get('page_all', '1'))
        	        page_type = request.GET.get('page_type')
        	except ValueError:
        	        page = 1
        	        page_all =1

		page_data = 2
		article_count = Article.objects.filter(date_publish__icontains=year+'-'+month).count()
        	if page == 1 and page_all == 1:
        	        page_all = article_count/page_data
        	        if article_count%page_data > 0:
        	                page_all = page_all+1
        	if page_type=='up':
        	        page = page-1
        	if page_type=='down':
        	        page = page+1

		article_all = Article.objects.filter(date_publish__icontains=year+'-'+month)


		article_list = getPage(request, article_count, article_all, page_data, page, page_all, page_type)


		distinct_date_list = Article.objects.distinct_date()
	except Exception as e:
		logger.error(e)

	return render(request, 'archive.html', locals())
	
#文件详情
def article(request):
	try:
		id = request.GET.get('id')
		article = Article.objects.get(pk=id)
		tags = article.tag.all()

		#显示评论信息
		comments = Comment.objects.filter(article=article).order_by('id')
		comment_list = []
		for comment in comments:
			for item in comment_list:
				if not hasattr(item, 'children_comment'):
					setattr(item, 'children_comment', [])
				if comment.pid==item:
					item.children_comment.append(comment)
			if comment.pid is None:
				comment_list.append(comment)

		#添加评论表单
		comment_form = Comment_form({'article':article})
		
	except Exception as e:
		logger.error(e)
	return render(request, 'article.html', locals())

#创建评论
def comment_post(request):
	try:
		comment_form = Comment_form(request.POST)
		comment_form.save()
		article = comment_form.cleaned_data['article']	
		id = article.id
	except Exception as e:
		logger.error(e)
	return HttpResponseRedirect('/article?id='+str(id))	

#注册
def do_reg(request):
	if request.method == "POST":
		reg_form = Reg_Form(request.POST)
		#在调用Form的cleaned_data方法前必须判断reg_form.is_valid()
		if reg_form.is_valid(): 
			user = User.objects.create(username=reg_form.cleaned_data["username"], email=reg_form.cleaned_data["email"], url=reg_form.cleaned_data["url"], password=make_password(reg_form.cleaned_data["password"]))
		#	user = User.objects.create(username=reg_form.cleaned_data["username"],
                #                    email=reg_form.cleaned_data["email"],
                #                    url=reg_form.cleaned_data["url"],
                #                    password=reg_form.cleaned_data["password"])
		user.save()
		return redirect('/')
	reg_form = Reg_Form()
	return render(request, 'reg.html', locals())

def do_login(request):
	if request.method=="POST":
		login_form = Login_Form(request.POST)
		if login_form.is_valid():
			username = login_form.cleaned_data['username']
			password = login_form.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				user.backend = 'django.contrib.auth.backends.ModelBackend' # 指定默认的登录验证方式
                    		login(request, user)
				return redirect('/')
			else:
				return render(request, "failure.html", locals())
			
	login_form = Login_Form()
	return render(request, 'login.html', locals())
