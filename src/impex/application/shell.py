from .init import main
from .driver import ImpexDriverHolder


def setup(env):
    db = env['registry']['db']
    env['main'] = main
    env['db'] = db
    env['drivers'] = ImpexDriverHolder(lambda: db)
    env['drivers'].generate_drivers()
