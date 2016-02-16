from .base import TabWidget


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
