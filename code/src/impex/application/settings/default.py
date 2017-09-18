from os.path import dirname


def make_settings(settings, paths):
    project(settings, paths)
    session(settings, paths)
    database(settings, paths)
    alembic(settings, paths)
    fanstatic(settings, paths)
    auth(settings, paths)
    logger(settings, paths)
    debug(settings, paths)


def session(settings, paths):
    settings['session.type'] = 'file'
    settings['session.key'] = 'needtochangethis'
    settings['session.secret'] = 'needtochangethistoo'
    settings['session.cookie_on_exception'] = True

    paths.set('session:data', 'data', 'data')
    paths.set('session:lock', 'lock', 'data')
    settings['session.data_dir'] = paths.get('session:data')
    settings['session.lock_dir'] = paths.get('session:lock')


def database(settings, paths):
    # ----------------------------------------
    # This is example postgresql configuration
    # ----------------------------------------
    # settings['db']['type'] = 'postgresql'
    # settings['db']['login'] = 'develop'
    # settings['db']['password'] = 'develop'
    # settings['db']['host'] = 'localhost'
    # settings['db']['port'] = '5432'

    paths.set('sqlite_db', 'data.db', 'data')
    settings['dburl'] = 'sqlite:///' + paths.get('sqlite_db')


def project(settings, paths):
    maindir = dirname(dirname(dirname(dirname(dirname(__file__)))))
    with paths.set('maindir', maindir, is_root=True) as maindir:
        with maindir.set('srcdir', 'src',) as srcdir:
            with srcdir.set('project', 'impex') as impex:

                with impex.set('app:teams', 'teams') as teams:
                    teams.set('app:teams:routing', 'routing.yaml')

                with impex.set('app:events', 'events') as events:
                    events.set('app:events:routing', 'routing.yaml')

                with impex.set('app:games', 'games') as games:
                    games.set('app:games:routing', 'routing.yaml')

                with impex.set('app:groups', 'groups') as groups:
                    groups.set('app:groups:routing', 'routing.yaml')

                with impex.set('app:admin', 'admin') as admin:
                    admin.set('app:admin:routing', 'routing.yaml')

                with impex.set('app:places', 'places') as places:
                    places.set('app:places:routing', 'routing.yaml')

                with impex.set('app:sliders', 'sliders') as sliders:
                    sliders.set('app:sliders:routing', 'routing.yaml')

                with impex.set('app:auth', 'auth') as auth:
                    auth.set('app:auth:routing', 'routing.yaml')

    with paths.set('data', 'data', 'maindir') as datadir:
        datadir.set('frontendini', 'frontend.ini')

    paths.set('application', 'application', 'project')
    paths.set('routing', 'routing.yaml', 'application')
    settings['ga'] = 'UA-15178164-3'
    settings['package_name'] = 'impex'


def alembic(settings, paths):
    paths.set('alembic:versions', 'migrations', 'maindir')
    paths.set('alembic:ini', 'alembic.ini', 'data')


def fanstatic(settings, paths):
    settings['fanstatic'] = {
        'bottom': True,
        'debug': True,
    }


def debug(settings, paths):
    settings['debug'] = True
    settings['pyramid.reload_templates'] = True
    settings['pyramid.debug_notfound'] = True
    settings['pyramid.debug_routematch'] = True


def auth(settings, paths):
    settings['auth_secret'] = 'somesecret'


def logger(settings, paths):
    settings['loggers'] = {
        'loggers': {
            'keys': 'root, sqlalchemy, alembic',
        },
        'handlers': {
            'keys': 'console',
        },
        'formatters': {
            'keys': 'generic',
        },
        'logger_root': {
            'level': 'INFO',
            'handlers': 'console',
        },
        'logger_sqlalchemy': {
            'level': 'INFO',
            'handlers': 'console',
            'qualname': 'sqlalchemy.engine',
            'propagate': '0',
        },
        'logger_alembic': {
            'level': 'INFO',
            'handlers': 'console',
            'qualname': 'alembic',
            'propagate': '0',
        },
        'handler_console': {
            'class': 'StreamHandler',
            'args': '(sys.stderr,)',
            'level': 'NOTSET',
            'formatter': 'generic',
        },
        'formatter_generic': {
            'format': '%%(asctime)s %%(levelname)-5.5s [%%(name)s][%%(threadName)s] %%(message)s',
        },
    }
