from mock import MagicMock
from mock import call
from mock import sentinel

from impex.application.testing import ControllerCase

from ..admin_controllers import GameCreateController
from ..admin_controllers import GameListController
from ..widgets import CreateGameFormWidget


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
