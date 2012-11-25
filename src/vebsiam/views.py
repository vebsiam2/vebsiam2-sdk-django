
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login as auth_login
from vebsiam.model import vebsiam_user
from vebsiam import vebsiam_config


def login(request):
    auth_login(request, vebsiam_user())
    print 'Login is for '+vebsiam_config.app_configuration['name']
    return HttpResponseRedirect(request.REQUEST['next'])

def logout(request):
    return HttpResponse("Logout Here")
