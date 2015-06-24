# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages

install_requires = [
    'impaf',

    'impaf-haml',
    'impaf-beaker',
    'impaf-sqlalchemy',
    'impaf-alembic',

    'waitress',
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
        entry_points=(
            '\n'.join([
                '[console_scripts]',
                'imalembic = impex.application.alembic:alembic',
                'iminitdb = impex.application.alembic:initdb',
                '[paste.app_factory]',
                'main = impex.application.init:main',
                ''
            ])
        ),
    )
