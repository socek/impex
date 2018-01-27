from impaf.testing import cache

from impex.application.testing import DriverCase
from impex.places.driver import PlaceDriver
from impex.places.models import Place


class TestDriverGroup(DriverCase):
    _object_cls = PlaceDriver

    @cache('module')
    def setUp(self):
        self.flush_table_from_object(Place)

        one = self.object().create(name='one')
        self.database().commit()

        return {
            'places': [one],
        }

    def test_list(self):
        self.setUp()

        data = [obj.name for obj in self.object().list()]

        assert data == ['one']
