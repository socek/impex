from impaf.testing import cache

from impex.application.testing import DriverCase
from impex.events.driver import Event
from impex.events.driver import EventDriver
from impex.teams.driver import Team
from impex.teams.driver import TeamDriver

from ..driver import Game
from ..driver import GameDriver


class TestDriverGame(DriverCase):
    _object_cls = GameDriver

    @cache
    def events(self):
        driver = EventDriver()
        driver.feed_database(self.database)
        return driver

    @cache
    def teams(self):
        driver = TeamDriver()
        driver.feed_database(self.database)
        return driver

    @cache('module')
    def setUp(self):
        self.flush_table_from_object(Game, Event, Team)

        teams = []
        teams.append(self.teams().create(name='first'))
        teams.append(self.teams().create(name='second'))
        teams.append(self.teams().create(name='third'))

        self.first_event = self.events().create(
            name='First Event',
        )
        self.second_event = self.events().create(
            name='Second Event',
        )
        self.database().commit()

        self.game_1 = self.object().create(
            event_id=self.first_event.id,
            left_id=teams[0].id,
            right_id=teams[1].id,
            priority=2,
        )
        self.game_2 = self.object().create(
            event_id=self.first_event.id,
            left_id=teams[2].id,
            right_id=teams[1].id,
            priority=3,
        )
        self.game_3 = self.object().create(
            event_id=self.first_event.id,
            left_id=teams[2].id,
            right_id=teams[0].id,
            priority=1,
        )
        self.game_4 = self.object().create(
            event_id=self.second_event.id,
            left_id=teams[0].id,
            right_id=teams[1].id,
            priority=1,
        )

        self.database().commit()
        return {
            'events': [self.first_event, self.second_event],
            'games': [self.game_1, self.game_2, self.game_3, self.game_4],
            'teams': teams,
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

    def test_find_by_priority(self):
        data = self.setUp()
        elements = self.object().find_by_priority(data['events'][0].id, 2)
        elements_id = [element.id for element in elements]

        assert [
            data['games'][0].id,
            data['games'][1].id
        ] == elements_id

    def test_is_double_positive(self):
        data = self.setUp()
        result = self.object().is_doubled(
            data['events'][0].id,
            data['teams'][0].id,
            data['teams'][1].id,
        )
        assert result is True

    def test_is_double_positive_reverse(self):
        data = self.setUp()
        result = self.object().is_doubled(
            data['events'][0].id,
            data['teams'][1].id,
            data['teams'][0].id,
        )
        assert result is True

    def test_is_double_negative(self):
        data = self.setUp()
        result = self.object().is_doubled(
            data['events'][1].id,
            data['teams'][2].id,
            data['teams'][1].id,
        )
        assert result is False

    def test_is_double_negative_except(self):
        data = self.setUp()
        result = self.object().is_doubled(
            data['events'][0].id,
            data['teams'][0].id,
            data['teams'][1].id,
            data['games'][0].id,
        )
        assert result is False

    def test_increment_priorities_by(self):
        try:
            data = self.setUp()
            game = self.object().get_by_id(data['games'][1].id)
            self.object().increment_priorities_by(
                data['events'][0].id,
                2,
                game,
            )
            self.database().commit()
            elements = self.object().list(data['events'][0].id)
            elements_id = [element.id for element in elements]

            assert [
                data['games'][2].id,
                data['games'][1].id,
                data['games'][0].id,
            ] == elements_id
        finally:
            del globals()['_module_cache']['setUp[]']
