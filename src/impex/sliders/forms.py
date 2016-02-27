from collections import namedtuple
from formskit.converters import ToBool

from .tabs import TabList
from impex.application.plugins.formskit import PostForm
from impex.application.testing import cache

TabTuple = namedtuple('Tabs', ['id', 'name'])


class SliderAdminForm(PostForm):

    @property
    @cache
    def tabs(self):
        return TabList(self.request).tabs

    def create_form(self):
        self.add_field(
            'refresh',
            label='Odśwież',
            validators=[],
        ).set_avalible_values(self._get_refresh_list)
        self.tab_data = list(self.drivers.tab_data.admin_list())
        for tab in self.tab_data:
            self.add_field(
                self._get_key(tab),
                label=tab.name,
                validators=[],
                convert=ToBool(),
            )

    def fill(self):
        for tab in self.tab_data:
            key = self._get_key(tab)
            self.set_value(key, tab.is_visible)

    def _get_key(self, tab):
        return 'is_visible-' + tab.name

    def on_success(self):
        data = self.get_data_dict(True)
        if data.get('refresh', ''):
            self.drivers.slider_event.create(
                name='refresh',
                value=data['refresh'],
            )

        for tab in self.tab_data:
            key = self._get_key(tab)
            tab.is_visible = data[key]

        self.database().commit()

    def _get_refresh_list(self):
        yield TabTuple('', '(brak)')
        for name, tab in self.tabs.items():
            yield TabTuple(name, tab.__class__.__name__)
