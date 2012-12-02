from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from vebsiam.model import vebsiam_user
from vebsiam import vebsiam_config, Users
from django.template.response import TemplateResponse
import httplib, urllib

def prod_login(request):
    c = httplib.HTTPConnection(vebsiam_config.server)
    c.request('GET', '/auth/login', headers={'connection':'close', 'host':request.META['HTTP_HOST']})
    res = c.getresponse()
    return HttpResponse(res.read(), status = res.status)
    
def dev_login(request):
    if(request.method == 'GET'):
        print {'next':request.REQUEST['next']}
        return TemplateResponse(request, 'vebsiam/dev/login.html', {'next':request.REQUEST['next'], 'error':None})
    elif (request.method == 'POST'):        
        if(Users.validate_user(request.POST['username'], request.POST['password'])):
            u = vebsiam_user()
            u.authenticated = True
            auth_login(request, u)
            print 'Login is for ' + vebsiam_config.app_configuration['name']
            return HttpResponseRedirect(request.REQUEST['next'])
        else:
            return TemplateResponse(request, 'vebsiam/dev/login.html',
                        {'next':request.REQUEST['next'], 'error':'Authentication Failed'})
    else:
        return HttpResponse("Method not implemented", status=410)

login = lambda request: vebsiam_config.server and prod_login(request) or dev_login(request)

def logout(request):
    auth_logout(request)
    return HttpResponse("Logout Here")
