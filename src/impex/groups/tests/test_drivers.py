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

        event1 = self.events().create(name='event')
        event2 = self.events().create(name='event2')

        one = self.object().create(name='one')
        two = self.object().create(name='two')
        three = self.object().create(name='three')
        four = self.object().create(name='four')
        self.database().commit()

        game = self.games().create(
            event_id=event1.id,
            priority=1,
            group_id=one.id,
        )
        self.database().commit()

        return {
            'groups': [one, two, three, four],
            'events': [event1, event2],
            'games': [game],
        }

    def test_list(self):
        self.setUp()

        data = [obj.name for obj in self.object().list()]

        assert data == ['one', 'two', 'three', 'four']

    def test_list_not_empty(self):
        data = self.setUp()

        result = [obj.name for obj in self.object().list_not_empty(data['events'][0].id)]

        assert result == ['one']

    def test_list_not_empty_for_empty_event(self):
        data = self.setUp()

        result = [obj.name for obj in self.object().list_not_empty(data['events'][1].id)]

        assert result == []
