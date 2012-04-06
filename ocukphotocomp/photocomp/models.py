# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#	 * Rearrange models' order
#	 * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class Person(models.Model):
	name = models.CharField(unique=True, max_length=255)
	id = models.AutoField(primary_key=True)
	def get_absolute_url(self):
		return "/people/"+self.name+"/"
	class Meta:
		db_table = u'people'
	def __unicode__(self):
		return self.name
	def best_entry(self):
		return self.entry_set.all().order_by('-total_score')[0]

class Season(models.Model):
	name = models.CharField(max_length=255)
	complete = models.BooleanField()
	id = models.AutoField(primary_key=True)
	def get_absolute_url(self):
		return "/seasons/"+self.name+"/"
	class Meta:
		db_table = u'seasons'
	def __unicode__(self):
		return self.name
	@staticmethod
	def latest():
		return Season.objects.all().order_by('-id')[0]

class Round(models.Model):
	theme = models.CharField(max_length=255)
	number = models.IntegerField()
	id = models.AutoField(primary_key=True)
	season = models.ForeignKey(Season, db_column='season')
	def get_absolute_url(self):
		return "/rounds/"+self.season.name+"/"+self.theme+"/"
	class Meta:
		db_table = u'rounds'
	def __unicode__(self):
		return self.season.name+" - "+self.theme
	def winner(self):
		return self.entry_set.all().order_by('-total_score')[0]

class Entry(models.Model):
	rank = int
	technical_score = models.SmallIntegerField()
	theme_score = models.SmallIntegerField()
	impact_score = models.SmallIntegerField()
	total_score = models.SmallIntegerField()
	id = models.AutoField(primary_key=True)
	person = models.ForeignKey(Person, db_column='person')
	round = models.ForeignKey(Round, db_column='round')
	comments = models.TextField()
	@property
	def image(self):
		return str(self.id)+"_"+self.round.season.name+"_"+self.round.theme+"_"+self.person.name
	@property
	def image_large(self):
		return self.image+"_FULL"
	@property
	def image_medium(self):
		return self.image+"_MEDIUM"
	@property
	def image_thumbnail(self):
		return self.image+"_THUMBNAIL"
	@property
	def image_squarethumbnail(self):
		return self.image+"_SQTHUMBNAIL"
	class Meta:
		db_table = u'entries'
	def __unicode__(self):
		return self.round.season.name+' - '+self.round.theme+' - '+self.person.name



