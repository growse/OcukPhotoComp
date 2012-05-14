import random
def debug_mode(request):
	from django.conf import settings
	return {'debug_mode': settings.DEBUG}

def photo_url(request):
	from django.conf import settings
	return {'photo_url': settings.PHOTO_URL,'cdn_url':settings.CDN_URL}

def season_list(request):
	from models import Season
	return {'seasons':Season.objects.all()}
