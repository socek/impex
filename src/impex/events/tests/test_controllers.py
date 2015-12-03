from mock import MagicMock
from mock import call

from impex.application.testing import ControllerCase

from ..controllers import EventListController


class TestEventListController(ControllerCase):
    _object_cls = EventListController

    def test_make(self):
        self.mdrivers()

        self.object().make()

        assert self.context() == {
            'events': self.mdrivers().events.list_for_user.return_value,
        }

    def test_set_breadcrumb(self):
        self.mroute_path()
        mock = MagicMock()
        self.object().set_crumbs(mock)

        mock.add_breadcrumb.assert_has_calls(
            [
                call(
                    'Główna',
                    None,
                    True
                ),
            ]
        )
