from mock import MagicMock
from mock import call
from mock import sentinel

from impaf.testing import cache

from impex.application.testing import ControllerCase

from ..controllers import TeamCreateController
from ..controllers import TeamEditController
from ..controllers import TeamListController
from ..widgets import CreateTeamFormWidget
from ..widgets import EditTeamFormWidget


class TestTeamListController(ControllerCase):
    _object_cls = TeamListController

    def test_make(self):
        self.mdrivers()

        self.object().make()

        assert self.context() == {
            'teams': self.mdrivers().teams.list.return_value,
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
                    'Drużyny',
                    None,
                    True,
                ),
            ]
        )


class TestTeamCreateController(ControllerCase):
    _object_cls = TeamCreateController

    def test_make_on_success(self):
        self.madd_form_widget().return_value.validate.return_value = True
        self.madd_flashmsg()
        self.mredirect()

        self.object().make()

        self.madd_form_widget().assert_called_once_with(CreateTeamFormWidget)
        self.madd_form_widget().return_value.validate.assert_called_once_with()
        self.madd_flashmsg().assert_called_once_with('Dodano drużynę.', 'info')
        self.mredirect().assert_called_once_with('teams:admin:list')

    def test_make_on_fail(self):
        self.madd_form_widget().return_value.validate.return_value = False
        self.madd_flashmsg()
        self.mredirect()

        self.object().make()

        self.madd_form_widget().assert_called_once_with(CreateTeamFormWidget)
        self.madd_form_widget().return_value.validate.assert_called_once_with()
        assert not self.madd_flashmsg().called
        assert not self.mredirect().called

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
                    'Drużyny',
                    self.mroute_path().return_value,
                ),
                call(
                    'Dodawanie',
                    None,
                    True,
                ),
            ]
        )


class TestTeamEditController(ControllerCase):
    _object_cls = TeamEditController

    def setUp(self):
        super().setUp()
        self.mdrivers()
        self.madd_flashmsg()
        self.mredirect()
        self.mmatchdict()['team_id'] = sentinel.team_id

    @cache
    def mteam(self):
        return self.mdrivers().teams.get_by_id.return_value

    def assert_team_id(self, team_id):
        self.mdrivers().teams.get_by_id.assert_called_once_with(
            team_id,
        )

    def test_make_on_success(self):
        self.mform_widget().validate.return_value = True

        self.object().make()

        self.mform_widget().read_from.assert_called_once_with(self.mteam())
        self.assert_team_id(sentinel.team_id)
        self.madd_form_widget().assert_called_once_with(EditTeamFormWidget)
        self.mform_widget().validate.assert_called_once_with()

        self.madd_flashmsg().assert_called_once_with(
            'Zapisano zmiany w drużunie.',
            'info',
        )
        self.mredirect().assert_called_once_with('teams:admin:list')

    def test_make_on_fail(self):
        self.mform_widget().validate.return_value = False

        self.object().make()

        self.mform_widget().read_from.assert_called_once_with(self.mteam())
        self.assert_team_id(sentinel.team_id)
        self.madd_form_widget().assert_called_once_with(EditTeamFormWidget)
        self.mform_widget().validate.assert_called_once_with()

        assert not self.madd_flashmsg().called
        assert not self.mredirect().called

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
                    'Drużyny',
                    self.mroute_path().return_value,
                ),
                call(
                    'Edycja',
                    None,
                    True,
                ),
            ]
        )
