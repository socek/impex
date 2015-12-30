from impaf.testing import cache

from impex.application.testing import DriverCase
from impex.events.driver import EventDriver
from impex.events.models import Event
from impex.games.driver import GameDriver
from impex.games.models import Game
from impex.groups.driver import GroupDriver
from impex.groups.models import Group


class TestDriverGroup(DriverCase):
    _object_cls = GroupDriver

    @cache
    def events(self):
        driver = EventDriver()
        driver.feed_database(self.database)
        return driver

    @cache
    def games(self):
        driver = GameDriver()
        driver.feed_database(self.database)
        return driver

    @cache('module')
    def setUp(self):
        self.flush_table_from_object(Game, Group, Event)

        event = self.events().create(name='event')

        one = self.object().create(name='one')
        two = self.object().create(name='two')
        three = self.object().create(name='three')
        four = self.object().create(name='four')
        self.database().commit()

        game = self.games().create(
            event_id=event.id,
            priority=1,
            group_id=one.id,
        )
        self.database().commit()

        return {
            'games': [one, two, three, four],
            'event': event,
            'games': game,
        }

    def test_list(self):
        self.setUp()

        data = [obj.name for obj in self.object().list()]

        assert data == ['one', 'two', 'three', 'four']

    def test_list_not_empty(self):
        data = self.setUp()

        data = [obj.name for obj in self.object().list_not_empty()]

        assert data == ['one']
