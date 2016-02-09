from implugin.jinja2.widget import SingleWidget

from impex.application.requestable import Requestable
from impex.application.testing import cache
from impex.games.widgets import GameWidget


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


class SlideshowTabWidget(TabWidget):
    host = 'http://localhost/images/'
    local_path = None
    template = 'impex.sliders:templates/widgets/slideshow.haml'

    def _get_images(self):
        for image in self.images:
            yield self.host + image

    def make(self):
        super().make()
        self.context['images'] = self._get_images()


class FirstTabWidget(SlideshowTabWidget):
    name = 'first'
    local_path = '/home/socek/zdjecia/mlk/do_gosi'
    speed = 2

    images = [
        '/do_gosi/IMG_0468.JPG',
        '/do_gosi/IMG_0469.JPG',
        '/do_gosi/IMG_0470.JPG',
        '/do_gosi/IMG_0471.JPG',
        '/do_gosi/IMG_0472.JPG',
        '/do_gosi/IMG_0474.JPG',
    ]


class SecondTabWidget(SlideshowTabWidget):
    name = 'second'
    local_path = '/home/socek/zdjecia/mlk/second'
    speed = 2


class ScoresTabWidget(TabWidget):
    name = 'scores'
    speed = 10
    template = 'impex.sliders:templates/widgets/scores.haml'

    @property
    @cache
    def event_id(self):
        return self.matchdict['event_id']

    @property
    @cache
    def event(self):
        return self.drivers.events.get_by_id(self.event_id)

    def make(self):
        super().make()
        self.context['games'] = self._generate_games()

    def _generate_games(self):
        query = self.drivers.games.list(self.event_id)
        for game in query:
            widget = GameWidget(game)
            widget.feed_request(self.request)
            yield widget

    def __call__(self, *args, **kwargs):
        self.make(*args, **kwargs)
        rer = self.render(self.get_template())
        return rer
