from pyramid.security import Allow
from pyramid.security import Authenticated
from pyramid.security import Deny
from pyramid.security import Everyone

from .requestable import Requestable


class EntryFactory(Requestable):
    __acl__ = [
        (Allow, Everyone, 'view'),
        (Deny, Authenticated, 'guest'),
        (Allow, Everyone, 'guest'),
        (Allow, Authenticated, 'auth'),
    ]

    def __init__(self, request):
        self.feed_request(request)
        self.user = self.get_user()
