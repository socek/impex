def make_settings(settings, paths):
    settings['debug'] = True
    paths.set_path('sqlite_db', 'data', '%(db:name)s.db')
    session(settings, paths)
    database(settings, paths)
    envoritment(settings, paths)


def session(settings, paths):
    settings['session.type'] = 'file'
    settings['session.key'] = 'needtochangethis'
    settings['session.secret'] = 'needtochangethistoo'
    settings['session.cookie_on_exception'] = True

    paths['session'] = {
        'data_dir': ["%(data)s", 'sessions', 'data'],
        'lock_dir': ["%(data)s", 'sessions', 'lock'],
    }
    settings['session.data_dir'] = '%(paths:session:data_dir)s'
    settings['session.lock_dir'] = '%(paths:session:lock_dir)s'


def database(settings, paths):
    # ----------------------------------------
    # This is example postgresql configuration
    # ----------------------------------------
    # settings['db']['type'] = 'postgresql'
    # settings['db']['login'] = 'develop'
    # settings['db']['password'] = 'develop'
    # settings['db']['host'] = 'localhost'
    # settings['db']['port'] = '5432'
    settings['db']['type'] = 'sqlite'
    settings['db']['name'] = '%(project)s_develop'
    paths.set_path('sqlite_db', 'data', '%(db:name)s.db')


def envoritment(settings, paths):
    paths.set_path('data', 'project', 'data')
