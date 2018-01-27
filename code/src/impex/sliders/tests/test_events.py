from mock import MagicMock

from impex.application.testing import RequestCase
from impex.application.testing import cache

from ..events import EventParser
from ..events import RefreshEvent


class ParserCase(RequestCase):

    @cache
    def parser(self):
        return self._object_cls(self.mrequest(), self.context())

    @cache
    def mevent(self):
        return MagicMock()


class TestEventParser(ParserCase):
    _object_cls = EventParser

    def test_simple(self):
        assert self.parser().context == self.context()
        assert self.parser().request == self.mrequest()
        self.parser().prepere()
        self.parser().parse(self.mevent())


class TestRefreshEvent(ParserCase):
    _object_cls = RefreshEvent

    def test_prepere(self):
        self.parser().prepere()
        assert self.parser().context == {'refresh': []}

    def test_parser(self):
        event = self.mevent()
        event.value = 'myname'
        self.parser().prepere()

        self.parser().parse(event)
        assert self.parser().context == {'refresh': ['myname']}

        self.parser().parse(event)
        assert self.parser().context == {'refresh': ['myname']}
