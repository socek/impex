from impex.application.init import mian


def setup(env):
    request = env['request']
    env['driver'] = request.driver
    env['db'] = env['request'].db
    env['main'] = main
