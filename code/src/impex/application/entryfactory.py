from pyramid.security import Allow
from pyramid.security import Authenticated
from pyramid.security import Deny
from pyramid.security import Everyone

from .requestable import Requestable


class EntryFactory(Requestable):
    @property
    def __acl__(self):
        acl = [
            (Allow, Everyone, 'view'),
            (Deny, Authenticated, 'guest'),
            (Allow, Everyone, 'guest'),
            (Allow, Authenticated, 'auth'),
        ]
        if self.user.is_admin:
            acl.append((Allow, Authenticated, 'admin'))
        return acl

    def __init__(self, request):
        self.feed_request(request)
        self.user = self.get_user()
