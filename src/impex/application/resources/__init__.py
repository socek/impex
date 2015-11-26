from fanstatic import Library, Resource

library = Library('bootstrap', '.')

bootstrap_js = Resource(library, 'bootstrap/js/bootstrap.min.js', bottom=True)
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
