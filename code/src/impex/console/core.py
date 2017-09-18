from os.path import dirname

from baelfire.core import Core

import impex

from impex.application.init import main


class ImpexCore(Core):

    def phase_settings(self):
        super().phase_settings()

        main._generate_settings({}, endpoint='command')

        self.settings.update(main.settings)
        self.paths.paths.update(main.paths.paths)

        cwd = dirname(dirname(dirname(impex.__file__)))

        self.paths.set('cwd', cwd, is_root=True)
        self.paths.set('package:src', 'src', 'cwd')
        self.paths.set('src', 'src', 'cwd')
        self.paths.set('package:main', 'impex', 'src')
        self.paths.set('package:console', 'console', 'package:main')
        self.paths.set('package:wwtemplates', 'templates', 'package:console')
        self.paths.set('package:application', 'application', 'package:main')
        self.paths.set('package:settings', 'settings', 'package:application')
        self.paths.set('data', 'data', 'cwd')

        self.paths.set('uwsgi:pidfile', 'uwsgi.pid', 'data')
        self.paths.set('uwsgi:logto', 'uwsgi.log', 'data')
        self.paths.set('uwsgi:daemonize2', 'uwsgi.daemonize.log', 'data')
        self.paths.set('uwsgi:socket', 'uwsgi.socket', 'data')
        self.paths.set('virtualenv:bin', '/usr/local/bin', is_root=True)
        self.paths.set('exe:pserve', 'pserve', 'virtualenv:bin')
        self.paths.set('exe:uwsgi', 'uwsgi', 'virtualenv:bin')

        self.paths.set(
            'template:ini',
            'frontendini.jinja2',
            'package:wwtemplates',
        )
        self.paths.set(
            'package:default',
            'default.py',
            'package:settings',
        )
        self.paths.set(
            'package:local',
            'local.py',
            'package:settings',
        )
        self.paths.set(
            'migrations',
            'migrations',
            'cwd',
        )
        self.paths.set(
            'versions',
            'versions',
            'migrations',
        )
        self.paths.set(
            'log_all',
            'all.log',
            'data',
        )
        self.paths.set('frontendini', 'frontend.ini', 'data')

    def get_project_dir(self):
        project_dir = __file__
        for index in range(2):
            project_dir = dirname(project_dir)
        return project_dir
