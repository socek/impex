from mock import MagicMock
from mock import call
from mock import sentinel

from impex.application.testing import ControllerCase

from ..admin_controllers import GameCreateController
from ..admin_controllers import GameEditController
from ..admin_controllers import GameEditScoresController
from ..admin_controllers import GameListController
from ..widgets import CreateGameFormWidget
from ..widgets import EditGameFormWidget
from ..widgets import ScoreBoardWidget


class TestGameListController(ControllerCase):
    _object_cls = GameListController

    def test_make(self):
        self.mdrivers()

        self.object().make()

        assert self.context() == {
            'games': self.mdrivers().games.list.return_value,
        }

    def test_set_breadcrumb(self):
        self.mroute_path()
        mock = MagicMock()
        self.object().set_crumbs(mock)

        mock.add_breadcrumb.assert_has_calls(
            [
                call(
                    'Główna',
                    self.mroute_path().return_value,
                ),
                call(
                    'Panel Administracyjny',
                    None,
                    True,
                ),
                call(
                    'Wydarzenia',
                    self.mroute_path().return_value,
                ),
                call(
                    'Mecze',
                    None,
                    True,
                )
            ]
        )


class TestGameCreateController(ControllerCase):
    _object_cls = GameCreateController

    def test_set_breadcrumb(self):
        self.mroute_path()
        mock = MagicMock()
        self.object().set_crumbs(mock)

        mock.add_breadcrumb.assert_has_calls(
            [
                call(
                    'Główna',
                    self.mroute_path().return_value,
                ),
                call(
                    'Panel Administracyjny',
                    None,
                    True,
                ),
                call(
                    'Wydarzenia',
                    self.mroute_path().return_value,
                ),
                call(
                    'Mecze',
                    self.mroute_path().return_value,
                ),
                call(
                    'Dodawanie',
                    None,
                    True,
                )
            ]
        )

    def test_make_on_success(self):
        self.matchdict()['event_id'] = sentinel.event_id
        self.madd_form_widget().return_value.validate.return_value = True
        self.madd_flashmsg()
        self.mredirect()

        self.object().make()

        self.madd_form_widget().assert_called_once_with(CreateGameFormWidget)
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

        self.object().make()

        self.madd_form_widget().assert_called_once_with(CreateGameFormWidget)
        self.madd_form_widget().return_value.validate.assert_called_once_with()
        assert not self.madd_flashmsg().called
        assert not self.mredirect().called


class TestGameEditController(ControllerCase):
    _object_cls = GameEditController

    def test_set_breadcrumb(self):
        self.mroute_path()
        mock = MagicMock()
        self.object().set_crumbs(mock)

        mock.add_breadcrumb.assert_has_calls(
            [
                call(
                    'Główna',
                    self.mroute_path().return_value,
                ),
                call(
                    'Panel Administracyjny',
                    None,
                    True,
                ),
                call(
                    'Wydarzenia',
                    self.mroute_path().return_value,
                ),
                call(
                    'Mecze',
                    self.mroute_path().return_value,
                ),
                call(
                    'Edycja',
                    None,
                    True,
                )
            ]
        )

    def test_make_on_success(self):
        self.matchdict()['event_id'] = sentinel.event_id
        self.matchdict()['game_id'] = sentinel.game_id
        self.madd_form_widget().return_value.validate.return_value = True
        self.madd_flashmsg()
        self.mredirect()
        self.mdrivers()

        self.object().make()

        self.madd_form_widget().assert_called_once_with(EditGameFormWidget)
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

    def test_make_on_fail(self):
        self.madd_form_widget().return_value.validate.return_value = False
        self.madd_flashmsg()
        self.mredirect()

        self.object().make()

        self.madd_form_widget().assert_called_once_with(EditGameFormWidget)
        self.madd_form_widget().return_value.validate.assert_called_once_with()
        assert not self.madd_flashmsg().called
        assert not self.mredirect().called


class TestGameEditScoresController(ControllerCase):
    _object_cls = GameEditScoresController

    def test_set_breadcrumb(self):
        self.mroute_path()
        mock = MagicMock()
        self.object().set_crumbs(mock)

        mock.add_breadcrumb.assert_has_calls(
            [
                call(
                    'Główna',
                    self.mroute_path().return_value,
                ),
                call(
                    'Panel Administracyjny',
                    None,
                    True,
                ),
                call(
                    'Wydarzenia',
                    self.mroute_path().return_value,
                ),
                call(
                    'Mecze',
                    self.mroute_path().return_value,
                ),
                call(
                    'Tabela wyników',
                    None,
                    True,
                )
            ]
        )

    def test_make_on_success(self):
        self.matchdict()['event_id'] = sentinel.event_id
        self.matchdict()['game_id'] = sentinel.game_id
        self.madd_form_widget().return_value.validate.return_value = True
        self.madd_flashmsg()
        self.mredirect()
        self.mdrivers()

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

    def test_make_on_fail(self):
        self.madd_form_widget().return_value.validate.return_value = False
        self.madd_flashmsg()
        self.mredirect()

        self.object().make()

        self.madd_form_widget().assert_called_once_with(ScoreBoardWidget)
        self.madd_form_widget().return_value.validate.assert_called_once_with()
        assert not self.madd_flashmsg().called
        assert not self.mredirect().called
