from setuptools import setup, find_packages
import sys, os

version = '0.0.1-dev'

setup(
    name='ckanext-redlink',
    version=version,
    description="Redlink",
    long_description='''
    ''',
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='David Riccitelli',
    author_email='david.riccitelli@redlink.co',
    url='http://redlink.co',
    license='APL',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['ckanext', 'ckanext.redlink'],
    include_package_data=True,
    zip_safe=False,
    entry_points='''
        [ckan.plugins]
        # Add plugins here, e.g.
        # myplugin=ckanext.redlink.plugin:PluginClass
        # example_iauthfunctions=ckanext.iauthfunctions.plugin:ExampleIAuthFunctionsPlugin
        redlink=ckanext.redlink.plugin:RedlinkPreview
    ''',
)
