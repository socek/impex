from mock import sentinel

from impaf.testing import cache

from impex.application.testing import ControllerCase

from ..admin_controllers import GroupCreateController
from ..admin_controllers import GroupEditController
from ..admin_controllers import GroupListController
from ..widgets import CreateGroupFormWidget
from ..widgets import EditGroupFormWidget


class TestGroupListController(ControllerCase):
    _object_cls = GroupListController

    def test_make(self):
        self.mdrivers()

        self.object().make()

        assert self.context() == {
            'groups': self.mdrivers().groups.list.return_value,
        }


class TestGroupCreateController(ControllerCase):
    _object_cls = GroupCreateController

    def test_make_on_success(self):
        self.madd_form_widget().return_value.validate.return_value = True
        self.madd_flashmsg()
        self.mredirect()

        self.object().make()

        self.madd_form_widget().assert_called_once_with(CreateGroupFormWidget)
        self.madd_form_widget().return_value.validate.assert_called_once_with()
        self.madd_flashmsg().assert_called_once_with('Dodano grupę.', 'info')
        self.mredirect().assert_called_once_with('groups:admin:list')

    def test_make_on_fail(self):
        self.madd_form_widget().return_value.validate.return_value = False
        self.madd_flashmsg()
        self.mredirect()

        self.object().make()

        self.madd_form_widget().assert_called_once_with(CreateGroupFormWidget)
        self.madd_form_widget().return_value.validate.assert_called_once_with()
        assert not self.madd_flashmsg().called
        assert not self.mredirect().called


class TestGroupEditController(ControllerCase):
    _object_cls = GroupEditController

    def setUp(self):
        super().setUp()
        self.mdrivers()
        self.madd_flashmsg()
        self.mredirect()
        self.mmatchdict()['group_id'] = sentinel.group_id

    @cache
    def mgroup(self):
        return self.mdrivers().groups.get_by_id.return_value

    def assert_group_id(self, group_id):
        self.mdrivers().groups.get_by_id.assert_called_once_with(
            group_id,
        )

    def test_make_on_success(self):
        self.mform_widget().validate.return_value = True

        self.object().make()

        self.mform_widget().read_from.assert_called_once_with(self.mgroup())
        self.assert_group_id(sentinel.group_id)
        self.madd_form_widget().assert_called_once_with(EditGroupFormWidget)
        self.mform_widget().validate.assert_called_once_with()

        self.madd_flashmsg().assert_called_once_with(
            'Zapisano zmiany w grupie.',
            'info',
        )
        self.mredirect().assert_called_once_with('groups:admin:list')

    def test_make_on_fail(self):
        self.mform_widget().validate.return_value = False

        self.object().make()

        self.mform_widget().read_from.assert_called_once_with(self.mgroup())
        self.assert_group_id(sentinel.group_id)
        self.madd_form_widget().assert_called_once_with(EditGroupFormWidget)
        self.mform_widget().validate.assert_called_once_with()

        assert not self.madd_flashmsg().called
        assert not self.mredirect().called
