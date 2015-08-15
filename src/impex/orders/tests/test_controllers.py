from mock import sentinel

from ..controllers import OrderCreateController
from ..controllers import OrderReadController
from ..controllers import OrdersListController
from ..forms import CreateForm
from impex.application.testing import ControllerCase


class TestOrdersListController(ControllerCase):
    _object_cls = OrdersListController

    def test_make(self):
        self.mdrivers()

        self.object().make()

        assert self.context() == {
            'orders': self.mdrivers().Orders.find_all.return_value,
        }


class TestOrderReadController(ControllerCase):
    _object_cls = OrderReadController

    def test_make(self):
        self.mdrivers()
        self.matchdict()['order_id'] = sentinel.order_id

        self.object().make()

        self.mdrivers().Orders.get_by_id.assert_called_once_with(
            sentinel.order_id
        )
        self.context()['order'] = self.mdrivers().Orders.get_by_id.return_value


class TestOrderCreateController(ControllerCase):
    _object_cls = OrderCreateController

    def test_make_form_not_valid(self):
        self.madd_form()
        self.mform().validate.return_value = False

        assert self.object().make() is None

        self.madd_form().assert_called_once_with(CreateForm)
        assert not self.mdatabase().return_value.commit.called

    def test_make_form_valid(self):
        self.madd_form()
        self.madd_flashmsg()
        self.mredirect()
        self.mform().validate.return_value = True

        assert self.object().make() is None

        self.madd_form().assert_called_once_with(CreateForm)
        self.mdatabase().return_value.commit.assert_called_once_with()
        self.madd_flashmsg().assert_called_once_with(
            'Dodano zamówienie.',
            'info',
        )
        self.mredirect().assert_called_once_with('orders:list')
