
class vebsiam_user(object):
    def __init__(self):
        self.id = 1
        self.backend = 'vebsiam.Users'
        self.username = 'Dummy User for now'
        self.authenticated = False
        
    def is_authenticated(self):
        return self.authenticated
    
    def save(self):
        pass
