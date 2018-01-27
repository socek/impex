from .base import TabWidget


class SlideshowTabWidget(TabWidget):
    host = 'http://turniejserv/'
    template = 'impex.sliders:templates/widgets/slideshow.haml'
    additional_css = 'text-center'

    def _get_images(self):
        for image in self.images:
            yield self.host + image

    def make(self):
        super().make()
        self.context['images'] = self._get_images()


class LogaTabWidget(SlideshowTabWidget):
    name = 'loga'
    speed = 4

    images = [
        'loga/balenx.gif',
        'loga/azaria.jpg',
        'loga/bi-med.png',
        'loga/bluvision.jpg',
        'loga/inicjatywa.gif',
        'loga/kbh_akord.png',
        'loga/kks.jpg',
        'loga/kurna_chata.jpg',
        'loga/manual_med.jpg',
        'loga/mk-tance.png',
        'loga/mtbs.png',
        'loga/noram.gif',
        'loga/oms.png',
        'loga/osatrans.jpg',
        'loga/parkwodny.png',
        'loga/proteko.jpg',
        'loga/remondis.gif',
        'loga/tck.jpg',
        'loga/terrabud.png',
        'loga/unimax.jpg',
        'loga/veolia.jpg',
        'loga/winnice-eurazji.jpg',
        'loga/zpomyslami.jpg',
    ]
