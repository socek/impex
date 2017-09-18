# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages

install_requires = [
    'impaf',

    'impaf-haml',
    'impaf-beaker',
    'impaf-sqlalchemy',
    'impaf-alembic',
    'impaf-fanstatic==0.1.1',
    'impaf-formskit==0.1.3',
    'impaf-flashmsg',
    'impaf-auth==0.1.1',

    'requests',
    'pytest',
    'js.jquery',
    'js.bootstrap',

    'waitress',
    'pyramid_debugtoolbar',
    'psycopg2',

    'baelfire',
    # 'css.fontawesome',
    'formskit==0.5.4.10',
    'freezegun',
    'fanstatic==1.0a5',
    'uwsgi',
    'fixdep',
    'python-twitter==3.0rc1',
]


if __name__ == '__main__':
    setup(
        name='impex',
        version='0.1',
        packages=find_packages('src'),
        package_dir={'': 'src'},
        install_requires=install_requires,
        include_package_data=True,
        entry_points={
            'fanstatic.libraries': (
                'home = impex.home.resources:library',
                'impex = impex.application.resources:library',
            ),
            'console_scripts': (
                'im-alembic = impex.application.alembic:alembic',
                'im-initdb = impex.application.alembic:initdb',
                'imcmd = impex.console.cmd:run',
            ),
            'paste.app_factory': (
                'main = impex.application.init:main',
            )
        }
    )
