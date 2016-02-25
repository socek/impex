from mock import sentinel

from impaf.testing import cache
from impex.application.testing import ControllerCase

from ..admin_controllers import BaseController
from ..admin_controllers import GameCreateController
from ..admin_controllers import GameEditController
from ..admin_controllers import GameEditScoresController
from ..admin_controllers import GameListController
from ..widgets import CreateGameFormWidget
from ..widgets import EditGameFormWidget
from ..widgets import ScoreBoardWidget


class BaseControllerCase(ControllerCase):

    @cache
    def mget_event(self):
        return self.pobject(self.object(), 'get_event')


class TestBaseController(ControllerCase):
    _object_cls = BaseController

    def test_get_event(self):
        self.matchdict()['event_id'] = sentinel.event_id
        self.mdrivers()

        result = self.object().get_event()
        assert result == self.mdrivers().events.get_by_id.return_value
        self.mdrivers().events.get_by_id.assert_called_once_with(
            sentinel.event_id
        )


class TestGameListController(BaseControllerCase):
    _object_cls = GameListController

    def test_make(self):
        self.mdrivers()

        self.object().make()

        assert self.context() == {
            'games': self.mdrivers().games.list.return_value,
        }


class TestGameCreateController(BaseControllerCase):
    _object_cls = GameCreateController

    def test_make_on_success(self):
        self.matchdict()['event_id'] = sentinel.event_id
        self.madd_form_widget().return_value.validate.return_value = True
        self.madd_flashmsg()
        self.mredirect()
        self.mget_event()

        self.object().make()

        self.madd_form_widget().assert_called_once_with(
            CreateGameFormWidget,
            event=self.mget_event().return_value,
        )
        self.madd_form_widget().return_value.validate.assert_called_once_with()
        self.madd_form_widget().return_value.fill.assert_called_once_with()
        self.madd_flashmsg().assert_called_once_with('Dodano mecz.', 'info')
        self.mredirect().assert_called_once_with(
            'games:admin:list',
            event_id=sentinel.event_id,
        )

    def test_make_on_fail(self):
        self.madd_form_widget().return_value.validate.return_value = False
        self.madd_flashmsg()
        self.mredirect()
        self.mget_event()

        self.object().make()

        self.madd_form_widget().assert_called_once_with(
            CreateGameFormWidget,
            event=self.mget_event().return_value,
        )
        self.madd_form_widget().return_value.validate.assert_called_once_with()
        assert not self.madd_flashmsg().called
        assert not self.mredirect().called


class TestGameEditController(BaseControllerCase):
    _object_cls = GameEditController

    def test_make_on_success(self):
        self.matchdict()['event_id'] = sentinel.event_id
        self.matchdict()['game_id'] = sentinel.game_id
        self.madd_form_widget().return_value.validate.return_value = True
        self.madd_flashmsg()
        self.mredirect()
        self.mdrivers()
        self.mget_event()
        self.mrefresh_scores()

        self.object().make()

        self.madd_form_widget().assert_called_once_with(
            EditGameFormWidget,
            event=self.mget_event().return_value,
        )
        self.madd_form_widget().return_value.validate.assert_called_once_with()
        self.madd_form_widget().return_value.read_from.assert_called_once_with(
            self.mdrivers().games.get_by_id.return_value,
        )
        self.mdrivers().games.get_by_id.assert_called_once_with(
            sentinel.game_id,
        )
        self.madd_flashmsg().assert_called_once_with(
            'Zapisano zmiany w meczu.',
            'info',
        )
        self.mredirect().assert_called_once_with(
            'games:admin:list',
            event_id=sentinel.event_id,
        )
        self.mrefresh_scores().assert_called_once_with()

    def test_make_on_fail(self):
        self.madd_form_widget().return_value.validate.return_value = False
        self.madd_flashmsg()
        self.mredirect()
        self.mget_event()

        self.object().make()

        self.madd_form_widget().assert_called_once_with(
            EditGameFormWidget,
            event=self.mget_event().return_value,
        )
        self.madd_form_widget().return_value.validate.assert_called_once_with()
        assert not self.madd_flashmsg().called
        assert not self.mredirect().called


class TestGameEditScoresController(BaseControllerCase):
    _object_cls = GameEditScoresController

    def test_make_on_success(self):
        self.matchdict()['event_id'] = sentinel.event_id
        self.matchdict()['game_id'] = sentinel.game_id
        self.madd_form_widget().return_value.validate.return_value = True
        self.madd_flashmsg()
        self.mredirect()
        self.mdrivers()
        self.mrefresh_scores()

        self.object().make()

        self.madd_form_widget().assert_called_once_with(ScoreBoardWidget)
        self.madd_form_widget().return_value.validate.assert_called_once_with()
        self.madd_form_widget().return_value.read_from.assert_called_once_with(
            self.mdrivers().games.get_by_id.return_value,
        )
        self.mdrivers().games.get_by_id.assert_called_once_with(
            sentinel.game_id,
        )
        self.madd_flashmsg().assert_called_once_with(
            'Zapisano tabelę wyników.',
            'info',
        )
        self.mredirect().assert_called_once_with(
            'games:admin:edit_scores',
            event_id=sentinel.event_id,
            game_id=sentinel.game_id,
        )
        self.mrefresh_scores()

    def test_make_on_fail(self):
        self.madd_form_widget().return_value.validate.return_value = False
        self.madd_flashmsg()
        self.mredirect()

        self.object().make()

        self.madd_form_widget().assert_called_once_with(ScoreBoardWidget)
        self.madd_form_widget().return_value.validate.assert_called_once_with()
        assert not self.madd_flashmsg().called
        assert not self.mredirect().called
