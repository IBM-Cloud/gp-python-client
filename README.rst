..  Copyright IBM Corp. 2015

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.

What is this?
-------------
``gp-python-client`` is the Python client for `Globalization Pipeline on IBM
Bluemix <https://www.ng.bluemix.net/docs/services/Globalization/index.html>`_.

IBM® Globalization provides machine translation and editing capabilities that
enable you to rapidly create, maintain, and revise translations for your
Bluemix™ application UI.  Use the intuitive Bluemix dashboard or full featured
RESTful API to seamlessly translate your English source strings in up to eight
other languages while continuing to develop, build, test, and deploy within
your Bluemix DevOps environment.

This package expands on the ``gettext`` module (avalible in the Python standard
library) and provides functionality for Python applications to use the
Globalization Pipeline service for translations.

Getting started
---------------
To get started, you should first become familiar with the service itself. A
good place to begin is by reading the `Getting Started with IBM Globalization
documentation
<https://www.ng.bluemix.net/docs/services/Globalization/index.html>`_.

The documentation explains how to create a new service instance, create
a new bundle, upload your source text and much more.

If you're impatient or just need a quick refresher...

**Create new Globalization Pipeline service instance:**

.. image:: https://ibm.box.com/shared/static/v59b5a19qjkfhxqaiwauz37nd9d8o8m2.gif
  :alt: Create new Globalization Pipeline service instance
  :width: 750
  :height: 400
  :align: left

**Create new bundle:**

.. image:: https://ibm.box.com/shared/static/8p2ytfm28smh29rl50c581gcfb4hsz8z.gif
  :alt: Create new bundle
  :width: 738
  :height: 483
  :align: left

Demo
----
This `demo Bluemix app
<http://gp-python-client-demo.mybluemix.net/>`_ uses the
Globalization Pipeline with the Python client to display a short welcome
message that is translated in several languages. The source code for the
demo can be found in the ``demo`` dir.

Installation
------------
To install ``gp-python-client``, simply run: ::

    $ pip install gp-python-client

Or if you're oldschool, run: ::

    $ easy_install gp-python-client


Examples
--------
**Example 1 - Bluemix app:**

This sample code will allow you to get started using the Globalization
Pipeline service in your Bluemix app. This example assumes the Bluemix app
has been binded with a service instance of Globalization Pipeline and
has a bundle named ``myBundle``, and that the bundle contains a source string
whose key is ``greet``. ::

    >>> from gpclient import GPClient, GPServiceAccount, GPTranslations
    >>> import locale
    >>>
    >>> acc = GPServiceAccount()
    >>> client = GPClient(acc)
    >>>
    >>> languages=[locale.getdefaultlocale()[0]] # languages=['fr_CA']
    >>>
    >>> t = client.translation(bundleId='myBundle', languages=languages)
    >>> _ = t.gettext # create alias for method
    >>>
    >>> print _('greet') # 'greet' key's French translated value will be used
    Bonjour
    >>>


**Example 2 - Non-Bluemix app:**

This sample code will allow you to get started using the Globalization
Pipeline service in a standalone Python app that is not hosted on Bluemix.
This example assumes there exists a service instance of Globalization
Pipeline that has a bundle named ``myBundle``, and that the bundle contains
a source string whose key is ``exit``.

You can find the Globalization Pipeline instance's ``url``, ``instanceId``,
``userId``, and ``password`` in the instance dashboard. It is recommended that
you create a new reader account and use it's credentials in your
applications. ::

    >>> from gpclient import GPClient, GPServiceAccount, GPTranslations
    >>> import locale
    >>>
    >>> acc = GPServiceAccount(url=url, instanceId=instId,
        userId=userId, password=passwd)
    >>> client = GPClient(acc)
    >>>
    >>> languages=[locale.getdefaultlocale()[0]] # languages=['es-mx']
    >>>
    >>> t = client.translation(bundleId='myBundle', languages=languages)
    >>> _ = t.gettext # create alias for method
    >>>
    >>> print _('exit') # 'exit' key's Spanish translated value will be used
    Adiós
    >>>


Obtaining language/locale codes
-------------------------------
This package requires that valid language/locale codes be
provided when asked; for example, when calling ``GPClient.translation()``
(see Examples). From these codes, the language, region, and script
subtags will be extracted.

Some example codes are: ::

    zh-Hans
    pt-BR
    ja
    en_US

There are several ways to get the code for the working locale. One way
is to use the ``locale`` module (avaliable as part of the Python standard
library). ::

    >>> import locale
    >>> myLocale = locale.getdefaultlocale()
    >>> print myLocale
    ('en_US', 'UTF-8')
    >>> code = myLocale[0]
    >>> print code
    en_US

From this example, the language code is ``en_US`` - where ``en`` is the
language subtag, and ``US`` is the region subtag.

API
---
The API documentation can be found `here
<http://pythonhosted.org/gp-python-client/>`_. If the link is broken, you
can generate documentation yourself. See below.

Generating documentation
------------------------
Documentation can be generated using ``Sphinx`` - you must first install it: ::

    $ pip install sphinx

Then, to auto generate the documentation, run: ::

    $ cd $BASEDIR/docs
    $ make clean
    $ make html

To navigate the documentation, open ``$BASEDIR/docs/_build/html/index.html``.

Creating distribution package
-----------------------------
First update ``CHANGES.txt`` and ``setup.py`` if necessary (e.g. update version
number), then create the preferred `distribution package
<http://python-packaging-user-guide.readthedocs.org/en/latest/distributing/#packaging-your-project>`_.

**Wheel distribution** (Recommended) ::

    $ pip install wheel
    $ python setup.py bdist_wheel

**Source distribution** ::

    $ python setup.py sdist

Note: Source distribution contains tests as well.

**Build distribution** ::

    $ python setup.py bdist

The new distribution files should be located under ``$BASEDIR/dist/``.

Running Tests
-------------
Refer to ``test/README.md``.

End Notes
------------
You are most welcome to `submit issues
<https://github.com/IBM-Bluemix/gp-python-client/issues>`_,
or `fork the repository
<https://github.com/IBM-Bluemix/gp-python-client>`_.

``gp-python-client`` is published under the `Apache License Version 2.0
<https://github.com/IBM-Bluemix/gp-python-client/blob/master/LICENSE.txt>`_.
