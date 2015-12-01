from impex.application.controller import Controller

from .widgets import CreateEventFormWidget
from .widgets import EditEventFormWidget


class EventListController(Controller):

    renderer = 'impex.events:templates/admin/list.haml'
    permission = 'admin'

    def make(self):
        self.context['events'] = self.drivers.events.list_for_admin()


class EventCreateController(Controller):

    renderer = 'impex.events:templates/admin/create.haml'
    permission = 'admin'

    def make(self):
        form = self.add_form_widget(CreateEventFormWidget)

        if form.validate():
            self.add_flashmsg('Dodano wydarzenie.', 'info')
            self.redirect('events:admin:list')


class EventEditController(Controller):

    renderer = 'impex.events:templates/admin/edit.haml'
    permission = 'admin'

    def make(self):
        event_id = self.matchdict['event_id']
        event = self.drivers.events.get_by_id(event_id)
        form = self.add_form_widget(EditEventFormWidget)
        form.read_from(event)

        if form.validate():
            self.add_flashmsg('Zapisano zmiany w wydarzeniu.', 'info')
            self.redirect('events:admin:list')
