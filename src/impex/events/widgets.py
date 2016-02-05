from implugin.jinja2.widget import SingleWidget

from impex.application.requestable import Requestable
from impex.application.plugins.formskit import FormWidget

from .forms import CreateEventForm
from .forms import EditEventForm


class CreateEventFormWidget(FormWidget):
    template = 'impex.events:templates/widgets/create_form.haml'
    form = CreateEventForm


class EditEventFormWidget(FormWidget):
    template = 'impex.events:templates/widgets/edit_form.haml'
    form = EditEventForm


class EventWidget(SingleWidget, Requestable):
    template = 'impex.events:templates/widgets/event.haml'

    def __init__(self, event):
        self.event = event

    def make(self):
        self.context['event'] = self.event
        self.context['groups'] = self.drivers.groups.list_not_empty(
            self.event.id
        )
        self.context['route_path'] = self.request.route_path
