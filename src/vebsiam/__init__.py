from django.conf.urls import patterns, url
from django.contrib.sessions.backends.base import SessionBase
import os, tempfile
from django.conf import settings
from django.utils.encoding import force_unicode
from vebsiam.model import vebsiam_user
import json


urlpatterns = patterns('',
    url('login', 'vebsiam.views.login'),
    url('logout', 'vebsiam.views.logout'),
    )

class VebsiamConfig(object):
    def __init__(self):
        self._session_dir = None
        self.app_configuration = json.load(file(getattr(settings,'VEBSIAM2_APP_CONFIGURATION','vebsiam2-app.json')))
        self.app_data = json.load(file(getattr(settings,'VEBSIAM2_APP_DATA','vebsiam2-auth-data.json')))
        
    def set_session_dir(self, sdir):
        if(os.path.isdir(sdir)):
            self._session_dir = sdir
        else:
            raise AttributeError()
    
    def get_session_dir(self):
        if(self._session_dir): 
            return self._session_dir
        self._session_dir = tempfile.mkdtemp('vebsiam_session')
        return self.session_dir
    
    def is_dev(self):
        return True
    
    session_dir = property(get_session_dir, set_session_dir)

vebsiam_config = VebsiamConfig()

class SessionStore(SessionBase):
    def exists(self, session_key):
        return os.path.isfile(os.path.join(vebsiam_config.session_dir, session_key))
    
    def create(self):
        while True:
            self._session_key = self._get_new_session_key()
            try:
                # Save immediately to ensure we have a unique entry in the
                # database.
                self.save(must_create=True)
            except:
                # Key wasn't unique. Try again.
                continue
            self.modified = True
            self._session_cache = {}
            return
    
    def load(self):
        try:
            data = file(os.path.join(vebsiam_config.session_dir, self._session_key), 'r').read()
            return self.decode(force_unicode(data))
        except:
            return {}

    def delete(self, session_key=None):
        try:
            os.unlink(os.path.join(vebsiam_config.session_dir, self._session_key))
        except:
            pass

    def save(self, must_create=False):
        session_key = self._get_or_create_session_key()
        if(os.path.isfile(os.path.join(vebsiam_config.session_dir, session_key)) and must_create):
            raise Exception()
        f = file(os.path.join(vebsiam_config.session_dir, session_key), 'w')
        f.write(self.encode(self._session_cache))
        f.close()

class Users(object):
    def get_user(self, user_key):
        u = vebsiam_user()
        u.authenticated = True
        return u
    
