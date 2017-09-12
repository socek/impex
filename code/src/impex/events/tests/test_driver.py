from datetime import date

from impex.application.testing import DriverCase
from impex.games.models import Game

from ..driver import Event
from ..driver import EventDriver


class TestDriverEvent(DriverCase):
    _object_cls = EventDriver

    def test_list_for_admin(self):
        self.flush_table_from_object(Game)
        self.flush_table_from_object(Event)
        self.object().create(name='one', start_date=date(2015, 1, 1))
        self.object().create(name='two', start_date=date(2014, 1, 1))
        self.object().create(name='three', start_date=date(2016, 1, 1))
        self.object().create(name='four', start_date=date(2012, 1, 1))
        self.database().commit()

        data = [obj.name for obj in self.object().list_for_admin()]

        assert data == ['three', 'one', 'two', 'four']

    def test_list_for_user(self):
        self.flush_table_from_object(Event)
        self.object().create(
            name='one',
            start_date=date(2015, 1, 1),
            is_visible=True,
        )
        self.object().create(
            name='two',
            start_date=date(2014, 1, 1),
            is_visible=False,
        )
        self.object().create(
            name='three',
            start_date=date(2016, 1, 1),
            is_visible=True,
        )
        self.object().create(
            name='four',
            start_date=date(2012, 1, 1),
        )
        self.database().commit()

        data = [obj.name for obj in self.object().list_for_user()]

        assert data == ['three', 'one']
