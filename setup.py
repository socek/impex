# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages

install_requires = [
    'impaf',

    'impaf-haml',
    'impaf-beaker',
    'impaf-sqlalchemy',
    'impaf-alembic',
    'impaf-fanstatic==0.1.1',
    'impaf-formskit==0.1.2',
    'impaf-flashmsg',
    'impaf-auth',

    'js.jquery',

    'waitress',
    'pyramid_debugtoolbar',
    'psycopg2',

    'baelfire==0.3.1',
    'bael.project==0.2',
    # 'css.fontawesome',
    'formskit==0.5.4.10',
    'freezegun',
]


def create_link(name, version):
    data = {
        'prefix': 'https://github.com/socek',
        'name': name,
        'version': version,
    }
    template = '%(prefix)s/%(name)s/tarball/master#egg=%(name)s-%(version)s'
    return template % data

dependency_links = [
    create_link('impaf', '0.1'),
    create_link('impaf-jinja2', '0.1'),
    create_link('impaf-haml', '0.1'),
    create_link('impaf-beaker', '0.1'),
    create_link('impaf-sqlalchemy', '0.1'),
    create_link('impaf-alembic', '0.1'),
    create_link('impaf-fanstatic', '0.1.1'),
    create_link('impaf-formskit', '0.1.2'),
    create_link('impaf-flashmsg', '0.1'),
    create_link('impaf-auth', '0.1'),

    create_link('bael.project', '0.2'),
    create_link('baelfire', '0.3.1'),
    create_link('formskit', '0.5.4.10'),
]

if __name__ == '__main__':
    setup(
        name='impex',
        version='0.1',
        packages=find_packages('src'),
        package_dir={'': 'src'},
        install_requires=install_requires,
        dependency_links=dependency_links,
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
