from impex.application.controller import Controller

from .widgets import CreateGroupFormWidget
from .widgets import EditGroupFormWidget


class GroupListController(Controller):

    renderer = 'impex.groups:templates/admin/list.haml'
    permission = 'admin'
    crumbs = 'groups:admin:list'

    def make(self):
        self.context['groups'] = self.drivers.groups.list()


class GroupCreateController(Controller):

    renderer = 'impex.groups:templates/admin/create.haml'
    permission = 'admin'
    crumbs = 'groups:admin:create'

    def make(self):
        form = self.add_form_widget(CreateGroupFormWidget)

        if form.validate():
            self.add_flashmsg('Dodano grupę.', 'info')
            self.redirect('groups:admin:list')


class GroupEditController(Controller):

    renderer = 'impex.groups:templates/admin/edit.haml'
    permission = 'admin'
    crumbs = 'groups:admin:edit'

    def make(self):
        group_id = self.matchdict['group_id']
        group = self.drivers.groups.get_by_id(group_id)
        form = self.add_form_widget(EditGroupFormWidget)
        form.read_from(group)

        if form.validate():
            self.add_flashmsg('Zapisano zmiany w grupie.', 'info')
            self.redirect('groups:admin:list')
