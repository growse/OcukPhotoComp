from django.contrib.sitemaps import Sitemap
from ocukphotocomp.photocomp.models import Season,Round,Person

class SeasonSitemap(Sitemap):
	changefreq = "weekly"
	priority = 0.7

	def items(self):
		return Season.objects.all()

class RoundSitemap(Sitemap):
	changefreq = "never"
	priority=0.5
	def items(self):
		return Round.objects.all()


class PersonSitemap(Sitemap):
	changefreq = "weekly"
	priority=0.5
	def items(self):
		return Person.objects.all()

class FlatSitemap(Sitemap):
	changefreq = "weekly"
	priority=0.8

	def items(self):
		return ['/']
	def location(self,obj):
		return obj
