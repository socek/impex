from mock import MagicMock
from mock import call
from mock import sentinel

from impex.application.testing import PostFormCase
from impex.application.testing import cache

from ..forms import SliderAdminForm


class TestSliderAdminForm(PostFormCase):
    _object_cls = SliderAdminForm

    @cache
    def mtab_list(self):
        return self.patch('impex.sliders.forms.TabList')

    @cache
    def mto_bool(self):
        return self.patch('impex.sliders.forms.ToBool')

    @cache
    def madd_field(self):
        return self.pobject(self.object(), 'add_field')

    def test_on_success(self):
        self.mdatabase()
        self.mdrivers()
        self.mdata().return_value = {
            'refresh': sentinel.refresh,
            'is_visible-myname': sentinel.myname,
        }
        tab = MagicMock()
        tab.name = 'myname'
        self.object().tab_data = [tab]

        self.object().on_success()

        self.mdata().assert_called_once_with(True)
        self.mdrivers().slider_event.create.assert_called_once_with(
            name='refresh',
            value=sentinel.refresh,
        )
        self.mdatabase().commit.assert_called_once_with()
        assert tab.is_visible == sentinel.myname

    def test_on_empty(self):
        self.mdatabase()
        self.mdrivers()
        self.mdata().return_value = {}

        self.object().on_success()

        self.mdata().assert_called_once_with(True)
        assert self.mdrivers().slider_event.create.called is False
        self.mdatabase().commit.assert_called_once_with()

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

    def test_create_form(self):
        tab = MagicMock()
        tab.name = 'kanada'
        tab.label = 'joko'
        self.mdrivers().tab_data.admin_list.return_value = [tab]
        self.madd_field()
        self.mto_bool()

        self.object().create_form()

        assert self.madd_field().call_args_list == [
            call('refresh', label='Odśwież', validators=[]),
            call(
                'is_visible-kanada',
                label='joko',
                convert=self.mto_bool().return_value,
                validators=[],
            ),
        ]

    def test_fill(self):
        tab = MagicMock()
        tab.name = 'myname'
        self.object().tab_data = [tab]
        self.mset_value()

        self.object().fill()

        self.mset_value().assert_called_once_with(
            'is_visible-myname',
            tab.is_visible,
        )
