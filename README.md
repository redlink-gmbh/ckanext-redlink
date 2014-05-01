ckanext-redlink - A CKAN extension for datasets hosted on Redlink
===========================================================================

This is a CKAN extension that provides *data preview* for datasets hosted on
[Redlink](http://redlink.co) using [SQUEBI](https://github.com/tkurz/squebi).

* Writing extensions tutorial:

    http://docs.ckan.org/en/latest/extensions/tutorial.html

* Custom theming tutorial:

    http://docs.ckan.org/en/latest/extensions/theming.html

    This is a work in progress, in the meantime provisional docs can be found
    here:

     http://docs.ckan.org/en/847-new-theming-docs/theming.html

* Example IDatasetForm:

   https://github.com/okfn/ckan/tree/master/ckanext/example_idatasetform


Requisites
==========

* An account and a published dataset on [Redlink](https://my.redlink.io/)
* A running CKAN 2 install (only version 2.2 has been tested so far)
* A sysadmin user
* Some datasets created


Installation
============

Install the extension as usual, in you activated virtualenv::

   pip install -e git+https://github.com/redlink-gmbh/ckanext-redlink.git.git#egg=ckanext-redlink

If you want to jump straight away to the end result, just add the plugin to
your CKAN configuration file::

    ckan.plugins = redlink

It is recommended though that you follow the individual steps as described in
the next section.

How it works
============

@@TODO@@

License
=======

[Apache License Version 2.0](LICENSE.txt)
