from django.shortcuts import render
import logging
from django.conf import settings

logger = logging.getLogger('logger_test')

def global_setting(request):
	return {'site_name':settings.SITE_NAME,
		'facebook':settings.FACEBOOK,}

# Create your views here.
def index(request):
	logger.debug('this is a debug')
	return render(request, 'index.html', locals())
