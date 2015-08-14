from mock import sentinel

from impaf.testing import PyTestCase
from impaf.testing import cache
from implugin.sqlalchemy.testing import SqlalchemyCase

from ..forms import CreateForm


class TestCreateForm(SqlalchemyCase, PyTestCase):
    _object_cls = CreateForm

    @cache
    def object(self, *args, **kwargs):
        self.mregistry()
        return self._object_cls(self.mrequest())

    @cache
    def mdata(self):
        return self.pobject(self.object(), 'get_data_dict')

    def test_make(self):
        self.mdrivers()
        self.mdata().return_value = {'name': sentinel.name}

        self.object().on_success()

        self.mdata().assert_called_once_with(True)
        self.mdrivers().Orders.create.assert_called_once_with(
            name=sentinel.name
        )
