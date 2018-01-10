from os import environ


def make_settings(settings, paths):
    database(settings, paths)
    project(settings, paths)
    twitter(settings, paths)


def database(settings, paths):
    settings['db']['type'] = 'postgresql'
    settings['db']['login'] = environ['DB_LOGIN']
    settings['db']['password'] = environ['DB_PASSWORD']
    settings['db']['host'] = environ['DB_HOST']
    settings['db']['port'] = '5432'
    settings['db']['name'] = environ['DB_NAME']
    paths.set_path('sqlite_db', 'data', '%(db:name)s.db')


def project(settings, paths):
    settings['main_url'] = environ['MAIN_URL']


def twitter(settings, paths):
    settings['consumer_key'] = environ['CONSUMER_KEY']
    settings['consumer_secret'] = environ['CONSUMER_SECRET']
    settings['access_token_key'] = environ['ACCESS_TOKEN_KEY']
    settings['access_token_secret'] = environ['ACCESS_TOKEN_SECRET']

