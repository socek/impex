from impex.application.testing import ControllerCase

from ..controllers import EventListController


class TestEventListController(ControllerCase):
    _object_cls = EventListController

    def test_make(self):
        self.mdrivers()

        self.object().make()

        assert self.context() == {
            'events': self.mdrivers().events.list_for_user.return_value,
            'groups': self.mdrivers().groups.list_not_empty.return_value,
        }
