<a href="http://redlink.co"><img src="http://redlink-gmbh.github.io/ckanext-redlink/images/banner.png" /></a>

ckanext-redlink - Redlink CKAN extension
===========================================================================

This is a CKAN extension that provides *data preview* for datasets hosted on
[Redlink](http://redlink.co) using [SQUEBI](https://github.com/tkurz/squebi).

Requisites
==========

* An account and a published dataset on [Redlink](https://my.redlink.io/)
* A running CKAN 2 install (only version 2.2 has been tested so far)
* A sysadmin user
* Some datasets created


Installation
============

Install the extension as usual, in you activated virtualenv:

    pip install -e git+https://github.com/redlink-gmbh/ckanext-redlink.git#egg=ckanext-redlink

If you want to jump straight away to the end result, just add the plugin to
your CKAN configuration file:

    ckan.plugins = redlink

Add add your Redlink [application key](http://dev.redlink.io/faq#get-key) to your CKAN configuration
file:

    [DEFAULT]
    redlink.app.key = <your-redlink-application-key>

It is recommended though that you follow the individual steps as described in
the next section.

How it works
============

@@TODO@@

License
=======

[Apache License Version 2.0](LICENSE.txt)
