from impaf.testing import cache

from impex.application.testing import DriverCase
from impex.events.driver import EventDriver, Event

from ..driver import Game
from ..driver import GameDriver


class TestDriverGame(DriverCase):
    _object_cls = GameDriver

    @cache
    def events(self):
        driver = EventDriver()
        driver.feed_database(self.database)
        return driver

    @cache('module')
    def setUp(self):
        self.flush_table_from_object(Game)
        self.flush_table_from_object(Event)

        self.first_event = self.events().create(
            name='First Event',
        )
        self.second_event = self.events().create(
            name='Second Event',
        )
        self.database().commit()

        self.game_1 = self.object().create(
            event_id=self.first_event.id,
            priority=2,
        )
        self.game_2 = self.object().create(
            event_id=self.first_event.id,
            priority=3,
        )
        self.game_3 = self.object().create(
            event_id=self.first_event.id,
            priority=1,
        )
        self.game_4 = self.object().create(
            event_id=self.second_event.id,
            priority=1,
        )

        self.database().commit()
        return {
            'events': [self.first_event, self.second_event],
            'games': [self.game_1, self.game_2, self.game_3, self.game_4],
        }

    def test_list(self):
        data = self.setUp()
        elements = self.object().list(data['events'][0].id)
        elements_id = [element.id for element in elements]

        assert [
            data['games'][2].id,
            data['games'][0].id,
            data['games'][1].id
        ] == elements_id

    def test_get_next_avalible_priority(self):
        data = self.setUp()
        result = self.object().get_next_avalible_priority(data['events'][0].id)
        assert result == 4
