from impex.application.requestable import Requestable


class EventParser(Requestable):

    name = None

    def __init__(self, request, context):
        self.feed_request(request)
        self.context = context

    def prepere(self):
        pass

    def parse(self, event):
        pass


class RefreshEvent(EventParser):
    name = 'refresh'

    def prepere(self):
        self.context['refresh'] = []

    def parse(self, event):
        value = event.value
        if value not in self.context['refresh']:
            self.context['refresh'].append(value)
