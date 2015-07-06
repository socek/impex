from mock import MagicMock

from pytest import fixture

from impaf.testing import RequestFixture

from ..forms import FirstForm


class TestFirstForm(RequestFixture):

    @fixture
    def form(self, mrequest, msession):
        return FirstForm(mrequest)

    @fixture
    def msession(self, mrequest):
        mrequest.session = MagicMock()
        return mrequest.session

    def test_success(self, form):
        assert form.on_success() is None
