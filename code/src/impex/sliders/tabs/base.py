from implugin.jinja2.widget import SingleWidget

from impex.application.requestable import Requestable


class TabWidget(SingleWidget, Requestable):
    name = None
    speed = 1
    additional_css = ''

    def make(self):
        self.context['name'] = self.name
        self.context['additional_css'] = self.additional_css

    def to_dict(self):
        return {
            'name': self.name,
            'speed': self.speed,
            'additional_css': self.additional_css,
        }
