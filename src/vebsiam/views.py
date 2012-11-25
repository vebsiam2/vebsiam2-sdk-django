
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from vebsiam.model import vebsiam_user
from vebsiam import vebsiam_config
from django.template.response import TemplateResponse

def login(request):
    if(request.method == 'GET'):
        print {'next':request.REQUEST['next']}
        return TemplateResponse(request, 'vebsiam/dev/login.html', {'next':request.REQUEST['next']})
    elif (request.method == 'POST'):
        u = vebsiam_user()
        u.authenticated = True
        auth_login(request, u)
        print 'Login is for ' + vebsiam_config.app_configuration['name']
        return HttpResponseRedirect(request.REQUEST['next'])
    else:
        return HttpResponse("Method not implemented", status=410)

def logout(request):
    auth_logout(request)
    return HttpResponse("Logout Here")
