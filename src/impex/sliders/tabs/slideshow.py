from .base import TabWidget


class SlideshowTabWidget(TabWidget):
    host = 'http://turniejserv/'
    template = 'impex.sliders:templates/widgets/slideshow.haml'

    def _get_images(self):
        for image in self.images:
            yield self.host + image

    def make(self):
        super().make()
        self.context['images'] = self._get_images()


class LogaTabWidget(SlideshowTabWidget):
    name = 'first'
    speed = 3

    images = [
        'loga/adencja.png',
        'loga/azaria.jpg',
        'loga/balnex.gif',
        'loga/bi-med.png',
        'loga/bluvision.jpg',
        'loga/fotografia-patryk.png',
        'loga/hi-tom.png',
        'loga/inivjatywa.gif',
        'loga/kks.jpg',
        'loga/mtbs.png',
        'loga/noram.gif',
        'loga/osa-trans.jpg',
        'loga/oscomputerosft.png',
        'loga/park_wodny.png',
        'loga/remondis.gif',
        'loga/tck.gif',
        'loga/terrabud.png',
        'loga/winnice-eurazji.jpg',
        'loga/zpomyslami.jpg',
    ]


class SecondTabWidget(SlideshowTabWidget):
    name = 'second'
    local_path = '/home/socek/zdjecia/mlk/second'
    speed = 2

