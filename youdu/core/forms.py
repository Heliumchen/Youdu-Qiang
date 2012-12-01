# encoding: utf-8
from django import forms
from django.db import models
from django.forms import ModelForm, TextInput
from django.utils.translation import ugettext_lazy as _

from youdu.core.models import *
		
class EventCreationForm(ModelForm):
	type = forms.ChoiceField(label=_(u"活动类型"),choices=EVENT_TYPES)
	title = forms.CharField(label=_(u"活动名称"),max_length=25,min_length=4,
		widget=forms.TextInput(attrs={'class': 'input-xlarge'}), required=True)
	site = forms.CharField(label=_(u"活动地点"),max_length=50,
		widget=forms.TextInput(attrs={'class': 'input-xlarge'}), required=True)
	start_time = forms.DateTimeField(label=_(u"活动时间"), required=True)
	link = forms.CharField(label=_(u"详情链接"),max_length=100,
		widget=forms.TextInput(attrs={'class': 'input-xlarge'}), required=False)
	designer = forms.CharField(label=_(u"设计者名称"),max_length=20,
		widget=forms.TextInput(attrs={'class': 'input-xlarge'}), required=True)
	poster = forms.ImageField(required=True)
	
	class Meta:
		model = Event
		fields = ('type','title','site','link','start_time','designer','poster')
