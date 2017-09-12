from implugin.jinja2.widget import SingleWidget

from impex.application.requestable import Requestable

from .models import BreadCrumb


class BreadCrumbsWidget(SingleWidget, Requestable):
    template = 'impex.breadcrumb:templates/main.haml'

    def __init__(self, controller):
        self.controller = controller

    def make(self):
        bread = BreadCrumb()
        bread.feed_request(self.request)
        name = getattr(self.controller, 'crumbs', None)

        self.context['bread'] = bread
        self.context['name'] = name
        self.context['crumbs'] = bread.get_crumbs_for(name)
