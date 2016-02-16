from implugin.jinja2.widget import SingleWidget

from impex.application.requestable import Requestable


class TabWidget(SingleWidget, Requestable):
    name = None
    speed = 1

    def make(self):
        self.context['name'] = self.name

    def to_dict(self):
        return {
            'name': self.name,
            'speed': self.speed,
        }
