from implugin.jinja2.widget import SingleWidget

from impex.application.requestable import Requestable

from .models import BreadCrumbElement


class BreadCrumbsWidget(SingleWidget, Requestable):
    template = 'impex.breadcrumb:templates/main.haml'

    def __init__(self, controller):
        self.controller = controller

    def add_breadcrumb(self, *args, **kwargs):
        self.context['crumbs'].append(BreadCrumbElement(*args, **kwargs))

    def make(self):
        self.context['crumbs'] = []
        method = getattr(self.controller, 'set_crumbs', lambda _: None)
        method(self)
