from photocomp.models import Season,Round,Entry,Person
from django.contrib import admin


class EntryInline(admin.TabularInline):
	model = Entry
	fields = ['comments','person','total_score','image']
	readonly_fields = ['person','image']
	extra = 0

class RoundAdmin(admin.ModelAdmin):
	fields = ['theme','number','season']
	inlines = [EntryInline]
	list_filter = ['season']
	search_fields = ['theme']

class EntryAdmin(admin.ModelAdmin):
	list_filter=['round']
	actions = ['generate_thumbnails']


admin.site.register(Season)
admin.site.register(Round,RoundAdmin)
admin.site.register(Entry,EntryAdmin)
admin.site.register(Person)
