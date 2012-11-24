
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login as auth_login
from vebsiam.model import vebsiam_user

def login(request):
    auth_login(request, vebsiam_user())
    return HttpResponseRedirect(request.REQUEST['next'])

def logout(request):
    return HttpResponse("Logout Here")
