from impex.application.controller import Controller


class EventListController(Controller):

    renderer = 'impex.events:templates/list.haml'

    def set_crumbs(self, widget):
        widget.add_breadcrumb('Główna', None, True)

    def make(self):
        self.context['events'] = self.drivers.events.list_for_user()
