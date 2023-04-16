from django.shortcuts import render
import os
import json

from oauthlib.oauth2 import TokenExpiredError
from requests_oauthlib import OAuth2Session
from django.http import HttpResponseRedirect

CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
REDIRECT_URI = os.environ['REDIRECT_URI']

oauth = OAuth2Session(CLIENT_ID,
                      redirect_uri=REDIRECT_URI,
                      scope=["read","write"])
authorization_url, state = oauth.authorization_url("https://ion.tjhsst.edu/oauth/authorize/")

# Create your views here.
def home(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html', {})
    else:
        return render(request, 'home.html', {})

def oauth_redirect(request):
    return HttpResponseRedirect(authorization_url)

def oauth_authorize(request):
    if "code" in request.GET:
        CODE = request.GET.get('code')
        STATE = request.GET.get('state')
        TOKEN = oauth.fetch_token("https://ion.tjhsst.edu/oauth/token/", code=CODE, client_secret=CLIENT_SECRET)
        profile = json.loads(oauth.get("https://ion.tjhsst.edu/api/profile").content.decode())
        print(profile.get('ion_username'))

    return render(request, 'home.html', {})