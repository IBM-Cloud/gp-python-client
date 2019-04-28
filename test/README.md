<!-- Copyright IBM Corp. 2015

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License. -->

Preparing Tests
-------------
To begin, you will first need to create a new Globalization Pipeline service
instance. Within this instance, create two new bundles:

**gpclient-test-1**

The first bundle should be called ``gpclient-test-1``.

Use the resource file ``data\gpclient-test-1-msgs.json`` and you must at least
include ``French`` and ``Spanish`` as target languages.

**gpclient-test-2**

The first bundle should be called ``gpclient-test-2``.

Use the resource file ``data\gpclient-test-2-msgs.json`` and you must at least
include ``French`` and ``Spanish`` as target languages.

Once the bundles are created, you need to update ``data/creds.json``.

Using service instance's Service Credentials section, create new IAM credentials for manager and reader role. You can find the ``url``, ``instanceId`` in the generated credentials. Use the ``apikey`` from manager role credentials for ``adminApiKey`. Use the ``apikey`` from reader role credentials for ``readerApiKey` `

GP reader (``readerUserId`` and ``readerPassword``) and admin (``userId`` and ``password``) account information
can be obtained by creating a new user. A new user can be
added in the service instance dashboard (``Manage > Users > New User``).

Once everything has been updated. Head to the next section.

Running Tests
-------------
Note: the commands below should be run while in the base dir, i.e.
``gp-python-client``.

To run the tests with only your current Python version, run:

    $ python setup.py test

To run tests with code coverage enabled, first install ``coverage``:

    $ pip install coverage

Then run:

    $ coverage run --source . setup.py test
    $ coverage report -m # cmd line report
    $ coverage html # html report

To run the tests under several Python versions, you will first need ``tox``:

    $ pip install tox

Then edit the ``tox.ini`` file as required, e.g. if you would like to run the
tests under Python 2.7 and 3.4, then ``envlist=py27, py34``. Note, you must
have these Python versions installed on your system. Once ``tox.ini`` is
updated, run:

    $ tox
