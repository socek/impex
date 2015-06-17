# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages

install_requires = [
    'impaf',

    'impaf-haml',
    'impaf-beaker',

    'waitress',
]
prefix = 'https://github.com/socek/'
dependency_links = [
    prefix + 'impaf/tarball/master#egg=impaf-0.1',
    prefix + 'impaf-jinja2/tarball/master#egg=impaf-jinja2-0.1',
    prefix + 'impaf-haml/tarball/master#egg=impaf-haml-0.1',
    prefix + 'impaf-beaker/tarball/master#egg=impaf-beaker-0.1',
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
                '[paste.app_factory]',
                'main = impex.application.init:main',
                ''
            ])
        ),
    )
