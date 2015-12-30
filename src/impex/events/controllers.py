from impex.application.controller import Controller


class EventListController(Controller):

    renderer = 'impex.events:templates/list.haml'
    crumbs = 'home'

    def make(self):
        self.context['events'] = self.drivers.events.list_for_user()
        self.context['groups'] = self.drivers.groups.list_not_empty()
