from pyramid.security import Allow
from pyramid.security import Authenticated
from pyramid.security import Everyone

from .requestable import Requestable


class EntryFactory(Requestable):
    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, Authenticated, 'auth_view'),
    ]

    def __init__(self, request):
        self.feed_request(request)
        user = self.get_user()
