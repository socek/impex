from collections import namedtuple

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

    def on_success(self):
        data = self.get_data_dict(True)
        if data.get('refresh', ''):
            self.drivers.slider_event.create(
                name='refresh',
                value=data['refresh'],
            )

            self.database().commit()

    def _get_refresh_list(self):
        yield TabTuple('', '(brak)')
        for name, tab in self.tabs.items():
            yield TabTuple(name, tab.__class__.__name__)
