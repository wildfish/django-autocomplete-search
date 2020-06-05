from setuptools import setup
import os
import re
import sys

import shutil

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search('__version__ = [\'"]([^\'"]+)[\'"]', init_py).group(1)

version = get_version('autocomplete_search')

if sys.argv[-1] == 'publish':
    if os.system('pip freeze | grep wheel'):
        print('wheel not installed.\nUse `pip install wheel`.\nExiting.')
        sys.exit()
    if os.system('pip freeze | grep twine'):
        print('twine not installed.\nUse `pip install twine`.\nExiting.')
        sys.exit()
    os.system('python setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')
    print('You probably want to also tag the version now:')
    print('  git tag -a {} -m \'version {}\''.format(version, version))
    print('  git push --tags')
    shutil.rmtree('dist')
    shutil.rmtree('build')
    shutil.rmtree('django_star_ratings.egg-info')
    sys.exit()


setup(
    name='django-autocomplete-search',
    version=version,
    packages=['autocomplete_search'],
    package_data={
        'autocomplete_search/static/autocomplete_search/dist': ['*'],
        'autocomplete_search/templates': ['*'],
    },
    include_package_data=True,
    url='https://github.com/wildfish/django-autocomplete-search',
    license='MIT',
    author='Dan Bate',
    author_email='developers@wildfish.com',
    description='Handles autocompleting text searches by model and field',
    long_description=README,
    install_requires=[
        'django<1.12',
        'django-haystack',
    ],
)
