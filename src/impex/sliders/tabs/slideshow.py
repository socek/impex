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
        'loga/azaria.jpg',
        'loga/balnex.gif',
        'loga/bi-med.png',
        'loga/eltar.png',
        'loga/fotografia-patryk.png',
        'loga/gwarek.gif',
        'loga/HI-TOM.png',
        'loga/inivjatywa.gif',
        'loga/integrac.gif',
        'loga/iph.gif',
        'loga/logo_bluvision.jpg',
        'loga/logo_parkwodny.png',
        'loga/logo-PWiK.jpg',
        'loga/mbm.gif',
        'loga/mosir.png',
        'loga/mtbs.png',
        'loga/noram.gif',
        'loga/osa_trans.jpg',
        'loga/oscomputerosft.png',
        'loga/ralk_big.gif',
        'loga/solver.png',
        'loga/ssg.png',
        'loga/tck.gif',
        'loga/terrabud.png',
        'loga/tgstacja.png',
        'loga/turniej_Manualmed_logo.jpg',
        'loga/tvs.jpg',
        'loga/veolia.jpg',
        'loga/winnice-eurazji.jpg',

    ]


class SecondTabWidget(SlideshowTabWidget):
    name = 'second'
    local_path = '/home/socek/zdjecia/mlk/second'
    speed = 2

