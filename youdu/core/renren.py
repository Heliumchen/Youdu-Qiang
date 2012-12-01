# encoding: utf-8
import datetime
from youdu.core.models import *
from django.contrib.auth.models import User

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404

from django.core.exceptions import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils import simplejson

import urllib
import hashlib

RENREN_APP_API_KEY = "YOUR_APP_KEY"
RENREN_APP_SECRET_KEY = "YOU_SECRET_KEY"

RENREN_AUTHORIZATION_URI = "http://graph.renren.com/oauth/authorize"
RENREN_ACCESS_TOKEN_URI = "http://graph.renren.com/oauth/token"
RENREN_REDIRECT_URI = "http://127.0.0.1:8000/login/renren"
RENREN_API_SERVER = "http://api.renren.com/restserver.do"

'''	
Renren Login
Last modified: 2011/11/05  @Author: Helium CHEN
'''
def renren_login(request):
	print 1
	args = dict(client_id=RENREN_APP_API_KEY, redirect_uri=RENREN_REDIRECT_URI)

	if 'error' in request.GET:
		msg = "%s\n%s\n%s\n" % (request.GET['error'], request.GET['error_description'], request.GET['error_uri'])
		return HttpResponse(msg)
	elif 'code' in request.GET:
		args["client_secret"] = RENREN_APP_SECRET_KEY
		args["code"] = request.GET['code']
		args["grant_type"] = "authorization_code"
		response = urllib.urlopen(RENREN_ACCESS_TOKEN_URI + "?" + urllib.urlencode(args)).read()
		access_token = simplejson.loads(response)["access_token"]
		#getLoggedInUser
		params = {"method": "users.getLoggedInUser"}
		api_client = RenRenAPIClient(access_token, RENREN_APP_SECRET_KEY)
		response = api_client.request(params);
		
		username = 'u%s_renren' % response["uid"]
		password = '%s#%s' % (username, RENREN_APP_SECRET_KEY)
		user = authenticate(username=username, password=password)
		if user is None:
			# Create a new user for this renren user
			params = {"method": "users.getInfo", "fields": "name,headurl,tinyurl"}
			response = api_client.request(params)			
			if type(response) is list:
				response = response[0]

			new_user = User.objects.create_user(username, '', password)
			new_user.first_name = response['name']
			new_user.save()
			profile = UserProfile(user = new_user, avatar=response['headurl'], small_avatar=response['tinyurl'])
			profile.save()
			user = authenticate(username=username, password=password)		
		login(request, user)
		return HttpResponseRedirect('/')
	else:
		args["response_type"] = "code"
		#args["scope"] = "publish_feed email status_update"
		url = RENREN_AUTHORIZATION_URI + "?" + urllib.urlencode(args)
		return HttpResponseRedirect(url)

class RenRenAPIClient(object):
    def __init__(self, access_token = None, secret_key = None):
        self.access_token = access_token
        self.secret_key = secret_key
    def request(self, params = None):
        """Fetches the given method's response returning from RenRen API.

        Send a POST request to the given method with the given params.
        """

        params["format"] = "json"
        params["access_token"] = self.access_token
        params["v"] = '1.0'
        sig = self.hash_params(params);
        params["sig"] = sig
        
        post_data = None if params is None else urllib.urlencode(params)
        file = urllib.urlopen(RENREN_API_SERVER, post_data)
        
        try:
            s = file.read()
            response = simplejson.loads(s)
        finally:
            file.close()
        if type(response) is not list and response.has_key("error_code"):
            raise RenRenAPIError(response["error_code"], response["error_msg"])
        return response
    def hash_params(self, params = None):
        hasher = hashlib.md5("".join(["%s=%s" % (self.unicode_encode(x), self.unicode_encode(params[x])) for x in sorted(params.keys())]))
        hasher.update(self.secret_key)
        return hasher.hexdigest()
    def unicode_encode(self, str):
        """
        Detect if a string is unicode and encode as utf-8 if necessary
        """
        return isinstance(str, unicode) and str.encode('utf-8') or str
    
class RenRenAPIError(Exception):
    def __init__(self, code, message):
        Exception.__init__(self, message)
        self.code = code
