import datetime
from django.utils import simplejson
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.db.models import Count,Sum,Avg
from django.http import Http404
from ocukphotocomp.photocomp.models import Season,Round,Person,Entry

def season(request,season_name=None):
        c=RequestContext(request)
	if season_name == None:
		season=Season.latest()
	else:
		season = get_object_or_404(Season,name=season_name)
	rounds = Round.objects.filter(season=season).order_by('number')
	if len(rounds)==0:
		return render_to_response('season.html',{'season':season},c)
	else:
		winner = None
		rounds = rounds.reverse()
		counter = 0
		while winner == None:
			latestround = rounds[counter]
			entries = Entry.objects.filter(round=latestround).order_by('-total_score')
			if len(entries) > 0:
				winner=entries[0]
			counter+=1
		seasonscores=Entry.objects.values('person__name','round__season').filter(round__season=season).annotate(total=Sum('total_score'), entered=Count('round')).order_by('-total')

		rank = 1
		previous = None
		seasonscores = list(seasonscores)
		previous = seasonscores[0]
		previous['rank'] = 1
		for i, entry in enumerate(seasonscores[1:]):
			if entry['total'] != previous['total']:
				rank = i + 2
				entry['rank'] = str(rank)
			else:
				entry['rank'] = "%s=" % rank
				previous['rank'] = entry['rank']
			previous = entry

		bestentry = None
		if season.complete:
			winner = Person.objects.all().filter(name=seasonscores[0]['person__name'])[0]
			bestentry = Entry.objects.all().filter(person=winner,round__season=season).order_by('-total_score')[0]
	
		return render_to_response('season.html',{'season':season,'rounds':rounds,'latestround':latestround,'winner':winner,'seasonscores':seasonscores,'bestentry':bestentry},c)

def round(request,season_name,round_theme):
	c=RequestContext(request)
	round = get_object_or_404(Round,theme=round_theme,season__name=season_name)
	entries = round.entry_set.all().order_by('-total_score')
	entries = list(entries)
	ranks = [0]*len(entries)
	rank = 1
	previous = None
	previous = entries[0]
	previous.rank = 1
	for i, entry in enumerate(entries[1:]):
		if entry.total_score != previous.total_score:
			rank = i + 2
			entry.rank = str(rank)
		else:
			entry.rank = "%s=" % rank
			previous.rank = entry.rank
		previous = entry
	return render_to_response('round.html',{'round':round,'entries':entries,'ranks':ranks},c)

def person (request,person_name):
	c=RequestContext(request)
	person = get_object_or_404(Person,name=person_name)
	entries = person.entry_set.all().order_by('-total_score')
	entriescount = entries.count()
	entriescountseason = entries.filter(round__season=Season.latest()).count()
	averagescore = entries.aggregate(Avg('total_score'))['total_score__avg']
	averagescoreseason = entries.filter(round__season=Season.latest()).aggregate(Avg('total_score'))['total_score__avg']
	return render_to_response('person.html',{'person':person,'entries':entries,'entriescount':entriescount,'entriescountseason':entriescountseason,'averagescore':averagescore,'averagescoreseason':averagescoreseason},c)

def search (request,term=None,helper=False):
	c=RequestContext(request)
	if term == None:
		if request.method == 'POST':
			return redirect("/search/"+request.POST.get('term','')+"/")
		else:
			return redirect("/",Permanent=True)
	else:
		rounds = Round.objects.all().filter(theme__istartswith=str(term))
		people = Person.objects.all().filter(name__istartswith=str(term))
		if helper==False:
			return render_to_response('search.html',{'rounds':rounds,'people':people,'term':term},c)
		else:
			json = []
			for round in rounds:
				json.append({"category":"Rounds","season":round.season.name,"value":round.theme,"label":round.theme+" ("+round.season.name+")"})
			for person in people:
				json.append({"category":"People","value":person.name,"label":person.name})

			return HttpResponse(simplejson.dumps(json))
