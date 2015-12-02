from fanstatic import Library, Resource

from implugin.fanstatic.resources import Resources as BaseResources

library = Library('bootstrap', '.')

bootstrap_js = Resource(
    library,
    'bootstrap/js/bootstrap.min.js',
    bottom=True,
)
bootstrap = Resource(
    library,
    'bootstrap/css/bootstrap.min.css',
    depends=[
        bootstrap_js,
    ]
)
custom = Resource(
    library,
    'bootstrap/css/custom.min.css',
    depends=[
        bootstrap_js,
    ]
)
datepicker_js = Resource(
    library,
    'bootstrap/js/bootstrap-datepicker.min.js',
    bottom=True,
)
datepicker_locale_pl = Resource(
    library,
    'bootstrap/locales/bootstrap-datepicker.pl.min.js',
    bottom=True,
)
datepicker = Resource(
    library,
    'bootstrap/css/datepicker.min.css',
    depends=[
        datepicker_js,
        datepicker_locale_pl,
    ]
)


class Resources(BaseResources):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_resource('home', 'impex.home.resources:home')
        self.add_resource(
            'bootstrap',
            'impex.application.resources:bootstrap',
        )
        self.add_resource(
            'custom',
            'impex.application.resources:custom',
        )
        self.add_resource(
            'datepicker',
            'impex.application.resources:datepicker',
        )
