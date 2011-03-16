from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from photocomp.models import Season,Round,Person,Entry
import zipfile, os.path, shutil

def bulkadd(request):
	thisround = Round.objects.all().order_by('-id')[0]
	resultstext = request.POST.get('resultstext')
	resultsarr = []
	if resultstext != None:
		results = resultstext.split("\n")
		if request.POST.get('assign')=='true':
			for result in results:
				result = result.replace("\t\t","\t")
				bits = result.split("\t")
				mapname = request.POST.get('map'+bits[0])
				person = None
				if mapname=='new':
					person = Person(name=bits[0])
					person.save()
				else:
					person=Person.objects.get(name=bits[0])
				thisentry=Entry(person=person,round=thisround,technical_score=bits[1],theme_score=bits[2],impact_score=bits[3],total_score=bits[4])
				thisentry.save()

			return HttpResponseRedirect("/cp/photocomp/round/")

		else:
			peopledropdown = ""
			peopledropdownarr = ["<option value=\"new\">(create new...)</option>"]
			for person in Person.objects.all().order_by('name'):
				peopledropdownarr.append('<option value="'+str(person.id)+'">'+person.name+'</option>')
			peopledropdown = ''.join(peopledropdownarr)
	
			for result in results:
				result = result.replace("\t\t","\t")
				bits = result.split("\t")
				if (len(bits)>=5):
					mapsto = bits[0]
					if Person.objects.filter(name=mapsto).exists()==False:
						mapsto = "<select name=\"map"+bits[0]+"\">"+peopledropdown+"</select>"
					resultsarr.append("<tr><td>"+bits[0]+"</td><td>"+mapsto+"</td><td>"+bits[1]+"</td><td>"+bits[2]+"</td><td>"+bits[3]+"</td><td>"+bits[4]+"</td></tr>")

	return render_to_response("admin/bulkadd.html", {
			'season':Season.latest(),
			'round':thisround,
			'resultstext':resultstext,
			'resultsarr':resultsarr
		}, RequestContext(request,{}))

def uploadimagezip(request):
	thisround = Round.objects.all().order_by('-id')[0]
	results = ""
	if request.method == 'POST':
		finalimagedir = '/var/www/growse.com/ocukimages/'
		f = request.FILES['zipfile']
		filename = f.name
		results+="Uploaded file is "+filename+"\n"
		directory='/tmp/ocukphotocomp/'
		if os.path.exists(directory):
			results+="dir exists, delete\n"
			shutil.rmtree(directory)
		results+="creating dir\n"
		os.mkdir(directory)
		fullpath = os.path.join(directory,filename)
		destination = open(fullpath,'wb+')
		results+="Saving file in "+fullpath+"\n"
		for chunk in f.chunks():
			destination.write(chunk)
		destination.close()

		
		# Get a real Python file handle on the uploaded file
		fullpathhandle = open(fullpath, 'r') 
		results+="Unzipping the file\n"
		# Unzip the file, creating subdirectories as needed
		zfobj = zipfile.ZipFile(fullpathhandle)
		for name in zfobj.namelist():
			if not name.endswith('/'):
				outfile = open(os.path.join(directory, name), 'wb')
				results+="Writing "+name+"\n"
				outfile.write(zfobj.read(name))
				outfile.close()
		for entry in thisround.entry_set.all():
			imagefile = entry.person.name+'.jpg'
			if os.path.exists(os.path.join(directory,imagefile)):
				results+="Found entry "+imagefile+"\n"
				newfilename = str(entry.id)+"_"+thisround.season.name+"_"+thisround.theme+"_"+entry.person.name+"_FULL.jpg"
				results+="Moving file to "+newfilename+"\n"
				shutil.move(os.path.join(directory,imagefile),os.path.join(finalimagedir,newfilename))
			else:
				results+="No image found for "+entry.person.name+"\n"
	return render_to_response("admin/uploadimagezip.html",{
			'season':thisround.season,
			'round':thisround,
			'results':results
		},RequestContext(request,()))

