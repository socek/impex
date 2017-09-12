from mock import MagicMock
from mock import sentinel

from impaf.testing import cache

from ..forms import CreateEventForm
from ..forms import EditEventForm
from impex.application.testing import PostFormCase


class TestCreateEventForm(PostFormCase):
    _object_cls = CreateEventForm

    def test_make(self):
        self.mdatabase()
        self.mdrivers()
        self.mdata().return_value = {
            'name': sentinel.name,
            'start_date': sentinel.start_date,
            'end_date': sentinel.end_date,
            'is_visible': '',
            'enable_twtitter': '',
        }

        self.object().on_success()

        self.mdata().assert_called_once_with(True)
        self.mdrivers().events.create.assert_called_once_with(
            name=sentinel.name,
            start_date=sentinel.start_date,
            end_date=sentinel.end_date,
            is_visible='',
            enable_twtitter='',
        )
        self.mdatabase().commit.assert_called_once_with()


class TestEditEventForm(PostFormCase):
    _object_cls = EditEventForm

    @cache
    def object(self):
        obj = super().object()
        obj.fields['start_date']._init_convert(None)
        obj.fields['end_date']._init_convert(None)
        return obj

    def test_make(self):
        self.mdatabase()
        self.mdrivers()
        self.minstance()
        self.mdata().return_value = {
            'name': sentinel.name,
            'start_date': sentinel.start_date,
            'end_date': sentinel.end_date,
            'is_visible': True,
            'enable_twtitter': False,
        }

        self.object().on_success()

        assert self.minstance().name == sentinel.name
        assert self.minstance().start_date == sentinel.start_date
        assert self.minstance().end_date == sentinel.end_date
        assert self.minstance().is_visible is True
        assert self.minstance().enable_twtitter is False
        self.mdrivers().events.update.assert_called_once_with(
            self.minstance()
        )

    def test_read_from(self):
        instance = MagicMock()
        instance.name = sentinel.name
        instance.start_date = sentinel.start_date
        instance.end_date = sentinel.end_date
        instance.is_visible = False
        instance.enable_twtitter = True

        self.object().read_from(instance)

        assert self.object().get_data_dict(True) == {
            'csrf_token': self.mget_csrf_token().return_value,
            'start_date': sentinel.start_date,
            'name': sentinel.name,
            'end_date': sentinel.end_date,
            'is_visible': False,
            'enable_twtitter': True,
        }

        assert self.object().instance is instance
