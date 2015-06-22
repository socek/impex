from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import AbstractConcreteBase

DeclarativeBase = declarative_base()


class Base(AbstractConcreteBase, DeclarativeBase):

    def __repr__(self):
        id_ = str(self.id) if self.id else 'None'
        return '%s (%s)' % (self.__class__.__name__, id_)

    def feed_request(self, request):
        self.request = request

    @property
    def settings(self):
        return self.registry['settings']

    @property
    def paths(self):
        return self.registry['paths']

    @property
    def registry(self):
        return self.request.registry
