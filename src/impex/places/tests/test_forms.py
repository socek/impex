from mock import MagicMock
from mock import sentinel

from impaf.testing import cache

from ..forms import CreatePlaceForm
from ..forms import EditPlaceForm
from impex.application.testing import PostFormCase


class TestCreatePlaceForm(PostFormCase):
    _object_cls = CreatePlaceForm

    def test_make(self):
        self.mdatabase()
        self.mdrivers()
        self.mdata().return_value = {
            'name': sentinel.name,
        }

        self.object().on_success()

        self.mdata().assert_called_once_with(True)
        self.mdrivers().places.create.assert_called_once_with(
            name=sentinel.name,
        )
        self.mdatabase().commit.assert_called_once_with()


class TestEditPlaceForm(PostFormCase):
    _object_cls = EditPlaceForm

    @cache
    def minstance(self):
        self.object().instance = MagicMock()
        return self.object().instance

    def test_make(self):
        self.mdatabase()
        self.mdrivers()
        self.minstance()
        self.mdata().return_value = {
            'name': sentinel.name,
        }

        self.object().on_success()

        assert self.minstance().name == sentinel.name
        self.mdrivers().places.update.assert_called_once_with(
            self.minstance()
        )

    def test_read_from(self):
        instance = MagicMock()
        instance.name = sentinel.name

        self.object().read_from(instance)

        assert self.object().get_data_dict(True) == {
            'csrf_token': self.mget_csrf_token().return_value,
            'name': sentinel.name,
        }

        assert self.object().instance is instance
