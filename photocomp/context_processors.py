import random

def photo_url(request):
	from django.conf import settings
	return {'photo_url': settings.PHOTO_URL}

def season_list(request):
	from models import Season
	return {'seasons':Season.objects.all()}
