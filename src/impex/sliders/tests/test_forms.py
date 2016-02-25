from mock import MagicMock
from mock import sentinel

from impex.application.testing import PostFormCase
from impex.application.testing import cache

from ..forms import SliderAdminForm


class TestSliderAdminForm(PostFormCase):
    _object_cls = SliderAdminForm

    @cache
    def mtab_list(self):
        return self.patch('impex.sliders.forms.TabList')

    def test_on_success(self):
        self.mdatabase()
        self.mdrivers()
        self.mdata().return_value = {
            'refresh': sentinel.refresh,
        }

        self.object().on_success()

        self.mdata().assert_called_once_with(True)
        self.mdrivers().slider_event.create.assert_called_once_with(
            name='refresh',
            value=sentinel.refresh,
        )
        self.mdatabase().commit.assert_called_once_with()

    def test_on_empty(self):
        self.mdatabase()
        self.mdrivers()
        self.mdata().return_value = {}

        self.object().on_success()

        self.mdata().assert_called_once_with(True)
        assert self.mdrivers().slider_event.create.called is False
        assert self.mdatabase().commit.called is False

    def test_get_refresh_list(self):
        self.mtab_list().return_value.tabs = {
            'name': MagicMock(),
        }

        data = list(self.object()._get_refresh_list())
        assert data[0].id == ''
        assert data[0].name == '(brak)'
        assert data[1].id == 'name'
        assert data[1].name == 'MagicMock'
        self.mtab_list().assert_called_once_with(self.mrequest())
