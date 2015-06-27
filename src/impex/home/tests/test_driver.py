from mock import MagicMock

from pytest import fixture

from ..driver import SampleDataDriver


class TestSampleDataDriver(object):

    @fixture
    def driver(self):
        return SampleDataDriver(MagicMock())
