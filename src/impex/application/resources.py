from fanstatic import Library, Resource

library = Library('bootstrap', 'resources')

bootstrap_js = Resource(library, 'bootstrap/js/bootstrap.min.js', bottom=True)
bootstrap = Resource(
    library,
    'bootstrap/css/bootstrap.min.css',
    depends=[
        bootstrap_js,
    ]
)
