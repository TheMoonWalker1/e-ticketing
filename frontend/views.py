from django.shortcuts import render, redirect
import os
import json

from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
User = get_user_model()

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

        username = profile.get('ion_username')
        email = profile.get('tj_email')
        sex = profile.get('sex')
        birthday = profile.get('birthday')
        nickname = profile.get('nickname')
        is_teacher = profile.get('is_teacher')
        is_student = profile.get('is_student')
        print(username)
        print(email)
        print(sex)
        print(birthday)
        print(nickname)
        print(is_student)
        try:
            print("log 1")
            login(request, User.objects.get(username=username))
        except User.DoesNotExist:
            print("log 2")
            user = User(username=username, email=profile.get('tj_email'), sex=profile.get('sex'), birthday=profile.get('birthday'), nickname=profile.get('nickname'), is_teacher=profile.get('is_teacher'), is_student=profile.get('is_student'))
            user.save()
            login(request, user)

    return redirect('home')

def oauth_logout(request):
    logout(request)
    return redirect('home')