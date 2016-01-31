from fanstatic import Library, Resource

from implugin.fanstatic.resources import Resources as BaseResources

library = Library('impex', '.')

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
timepicker_js = Resource(
    library,
    'bootstrap/js/bootstrap-timepicker.min.js',
    bottom=True,
)
timepicker = Resource(
    library,
    'bootstrap/css/bootstrap-timepicker.min.css',
    depends=[
        timepicker_js,
    ]
)
bracket_css = Resource(
    library,
    'bracket/jquery.bracket.min.css',
)

fontawesome = Resource(
    library,
    'fontawesome/css/font-awesome.min.css',
)

select2_js = Resource(
    library,
    'select2/js/select2.min.js',
    bottom=True,
)

select2_locale_pl = Resource(
    library,
    'select2/js/i18n/pl.js',
    bottom=True,
)

select2 = Resource(
    library,
    'select2/css/select2.min.css',
    depends=[
        select2_js,
        select2_locale_pl,
    ]
)

scoretable = Resource(
    library,
    'js/scoretable.js',
    bottom=True,
)

gamelist = Resource(
    library,
    'js/gamelist.js',
    bottom=True,
)

bracket = Resource(
    library,
    'bracket/jquery.bracket.min.js',
    depends=[
        bracket_css,
    ],
    bottom=True,
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
        self.add_resource(
            'fontawesome',
            'impex.application.resources:fontawesome',
        )
        self.add_resource(
            'timepicker',
            'impex.application.resources:timepicker',
        )
        self.add_resource(
            'select2',
            'impex.application.resources:select2',
        )
        self.add_resource(
            'scoretable',
            'impex.application.resources:scoretable',
        )
        self.add_resource(
            'gamelist',
            'impex.application.resources:gamelist',
        )
        self.add_resource(
            'bracket',
            'impex.application.resources:bracket',
        )
