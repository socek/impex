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
        'loga/noram.gif',
        'loga/remondis.gif',
        'loga/veolia.jpg',
        'loga/mtbs.png',
        'loga/logo-mzkp-ee.png',
        'loga/bluvision.jpg',
        'loga/cafe-silesia.png',
        'loga/azaria.jpg',
        'loga/parkwodny.png',
        'loga/kbh_akord.png',
        'loga/osatrans.jpg',
        'loga/logo-intergaz.png',
        'loga/bi-med.png',
        'loga/proteko.jpg',
        'loga/oms.png',
        'loga/tck.jpg',
        'loga/kurna_chata.jpg',
        'loga/kks.jpg',
        'loga/manual_med.jpg',
        'loga/mk-tance.png',
        'loga/inicjatywa.gif',
        'loga/winnice-eurazji.jpg',
        'loga/zpomyslami.jpg',
    ]
