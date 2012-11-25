
class vebsiam_user(object):
    def __init__(self):
        self.id = 1
        self.backend = 'vebsiam.Users'
        self.username = 'Dummy User for now'
        
    def is_authenticated(self):
        return True
    
    def save(self):
        pass
