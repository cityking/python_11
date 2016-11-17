from django.shortcuts import render
import logging
from django.conf import settings
from models import Category

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
	category_list = Category.objects.all()	
	logger.debug('this is a debug')
	return render(request, 'index.html', {"category_list" : category_list})
