# encoding: utf-8
import datetime
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import *
from django.core.exceptions import *

from django.core.files.images import ImageFile

from youdu.core.forms import *
from youdu.core.helper import *


def home(request):
	today = datetime.date.today()
	delta = datetime.timedelta(days=7)
	recent = today + delta
	later = recent + delta
	
	recent_events = Event.objects.filter(start_time__gte=today, start_time__lte=recent).order_by('start_time')
	#recent_events = Event.objects.all()
	return render_to_response('index.html', {'recent_events':recent_events,'today':today,'recent':recent,'later':later}, context_instance=RequestContext(request))
	
def submit_poster(request):
	if request.method == 'GET':
		form = EventCreationForm()
	elif request.method == 'POST':
		form = EventCreationForm(request.POST, request.FILES)
		print request.FILES['poster']
		if form.is_valid():
			new_event = form.save(commit=False)
			new_event.user_post = request.user
			img_file = get_thumbnail(request.FILES['poster'], request.FILES['poster'].name)
			new_event.small_poster.save(request.FILES['poster'].name, img_file, save=False)
			new_event.save()
			print 'saved'
			return HttpResponseRedirect('/')
	return render_to_response('submit_poster.html', {'form':form},context_instance=RequestContext(request))
	
def show_poster(request, poster_id):
	try:
		event = Event.objects.get(id=poster_id)
	except Event.DoesNotExist:
		raise Http404
	return render_to_response('poster.html', {'event':event},context_instance=RequestContext(request))
	
	
