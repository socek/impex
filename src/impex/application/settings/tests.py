def make_settings(settings, paths):
    database(settings, paths)


def database(settings, paths):
    settings['db']['type'] = 'postgresql'
    settings['db']['login'] = 'develop'
    settings['db']['password'] = 'develop'
    settings['db']['host'] = 'localhost'
    settings['db']['port'] = '5432'
    settings['db']['name'] = '%(project)s_tests'
