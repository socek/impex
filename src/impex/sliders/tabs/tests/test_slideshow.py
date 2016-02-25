from impex.application.testing import RequestCase
from impex.application.testing import cache

from ..slideshow import SlideshowTabWidget


class ExampleSlideshowTabWidget(SlideshowTabWidget):
    host = 'http://something.com/'
    images = [
        'something.jpg',
    ]
    name = 'myname'


class TestSlidershowTabWidget(RequestCase):

    @cache
    def tab_widget(self):
        widget = ExampleSlideshowTabWidget()
        widget.feed_request(self.mrequest())
        return widget

    def test_simple(self):
        self.tab_widget().make()
        context = self.tab_widget().context
        context['images'] = list(context['images'])

        assert context == {
            'images': ['http://something.com/something.jpg'],
            'name': 'myname',
            'request': self.mrequest(),
            'widget': self.tab_widget(),
        }
