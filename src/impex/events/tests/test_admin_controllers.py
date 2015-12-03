from mock import MagicMock
from mock import call
from mock import sentinel

from impaf.testing import cache

from impex.application.testing import ControllerCase

from ..admin_controllers import EventCreateController
from ..admin_controllers import EventEditController
from ..admin_controllers import EventListController
from ..widgets import CreateEventFormWidget
from ..widgets import EditEventFormWidget


class TestEventListController(ControllerCase):
    _object_cls = EventListController

    def test_make(self):
        self.mdrivers()

        self.object().make()

        assert self.context() == {
            'events': self.mdrivers().events.list_for_admin.return_value,
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
                    None,
                    True,
                ),
            ]
        )


class TestEventCreateController(ControllerCase):
    _object_cls = EventCreateController

    def test_make_on_success(self):
        self.madd_form_widget().return_value.validate.return_value = True
        self.madd_flashmsg()
        self.mredirect()

        self.object().make()

        self.madd_form_widget().assert_called_once_with(CreateEventFormWidget)
        self.madd_form_widget().return_value.validate.assert_called_once_with()
        self.madd_flashmsg().assert_called_once_with('Dodano wydarzenie.', 'info')
        self.mredirect().assert_called_once_with('events:admin:list')

    def test_make_on_fail(self):
        self.madd_form_widget().return_value.validate.return_value = False
        self.madd_flashmsg()
        self.mredirect()

        self.object().make()

        self.madd_form_widget().assert_called_once_with(CreateEventFormWidget)
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
                    'Wydarzenia',
                    self.mroute_path().return_value,
                ),
                call(
                    'Dodawanie',
                    None,
                    True,
                ),
            ]
        )


class TestEventEditController(ControllerCase):
    _object_cls = EventEditController

    def setUp(self):
        super().setUp()
        self.mdrivers()
        self.madd_flashmsg()
        self.mredirect()
        self.mmatchdict()['event_id'] = sentinel.event_id

    @cache
    def mevent(self):
        return self.mdrivers().events.get_by_id.return_value

    def assert_event_id(self, event_id):
        self.mdrivers().events.get_by_id.assert_called_once_with(
            event_id,
        )

    def test_make_on_success(self):
        self.mform_widget().validate.return_value = True

        self.object().make()

        self.mform_widget().read_from.assert_called_once_with(self.mevent())
        self.assert_event_id(sentinel.event_id)
        self.madd_form_widget().assert_called_once_with(EditEventFormWidget)
        self.mform_widget().validate.assert_called_once_with()

        self.madd_flashmsg().assert_called_once_with(
            'Zapisano zmiany w wydarzeniu.',
            'info',
        )
        self.mredirect().assert_called_once_with('events:admin:list')

    def test_make_on_fail(self):
        self.mform_widget().validate.return_value = False

        self.object().make()

        self.mform_widget().read_from.assert_called_once_with(self.mevent())
        self.assert_event_id(sentinel.event_id)
        self.madd_form_widget().assert_called_once_with(EditEventFormWidget)
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
                    'Wydarzenia',
                    self.mroute_path().return_value,
                ),
                call(
                    'Edycja',
                    None,
                    True,
                ),
            ]
        )
