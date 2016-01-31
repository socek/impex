from mock import sentinel

from impaf.testing import cache

from impex.application.testing import ControllerCase

from ..admin_controllers import PlaceCreateController
from ..admin_controllers import PlaceEditController
from ..admin_controllers import PlaceListController
from ..widgets import CreatePlaceFormWidget
from ..widgets import EditPlaceFormWidget


class TestPlaceListController(ControllerCase):
    _object_cls = PlaceListController

    def test_make(self):
        self.mdrivers()

        self.object().make()

        assert self.context() == {
            'places': self.mdrivers().places.list.return_value,
        }


class TestPlaceCreateController(ControllerCase):
    _object_cls = PlaceCreateController

    def test_make_on_success(self):
        self.madd_form_widget().return_value.validate.return_value = True
        self.madd_flashmsg()
        self.mredirect()

        self.object().make()

        self.madd_form_widget().assert_called_once_with(CreatePlaceFormWidget)
        self.madd_form_widget().return_value.validate.assert_called_once_with()
        self.madd_flashmsg().assert_called_once_with('Dodano miejsce.', 'info')
        self.mredirect().assert_called_once_with('places:admin:list')

    def test_make_on_fail(self):
        self.madd_form_widget().return_value.validate.return_value = False
        self.madd_flashmsg()
        self.mredirect()

        self.object().make()

        self.madd_form_widget().assert_called_once_with(CreatePlaceFormWidget)
        self.madd_form_widget().return_value.validate.assert_called_once_with()
        assert not self.madd_flashmsg().called
        assert not self.mredirect().called


class TestPlaceEditController(ControllerCase):
    _object_cls = PlaceEditController

    def setUp(self):
        super().setUp()
        self.mdrivers()
        self.madd_flashmsg()
        self.mredirect()
        self.mmatchdict()['place_id'] = sentinel.place_id

    @cache
    def mplace(self):
        return self.mdrivers().places.get_by_id.return_value

    def assert_place_id(self, place_id):
        self.mdrivers().places.get_by_id.assert_called_once_with(
            place_id,
        )

    def test_make_on_success(self):
        self.mform_widget().validate.return_value = True

        self.object().make()

        self.mform_widget().read_from.assert_called_once_with(self.mplace())
        self.assert_place_id(sentinel.place_id)
        self.madd_form_widget().assert_called_once_with(EditPlaceFormWidget)
        self.mform_widget().validate.assert_called_once_with()

        self.madd_flashmsg().assert_called_once_with(
            'Zapisano zmiany w miejscu.',
            'info',
        )
        self.mredirect().assert_called_once_with('places:admin:list')

    def test_make_on_fail(self):
        self.mform_widget().validate.return_value = False

        self.object().make()

        self.mform_widget().read_from.assert_called_once_with(self.mplace())
        self.assert_place_id(sentinel.place_id)
        self.madd_form_widget().assert_called_once_with(EditPlaceFormWidget)
        self.mform_widget().validate.assert_called_once_with()

        assert not self.madd_flashmsg().called
        assert not self.mredirect().called
