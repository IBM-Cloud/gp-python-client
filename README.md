<!-- Copyright IBM Corp. 2015, 2016

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License. -->

gp-python-client
----------------
`gp-python-client` is the official Python client for [IBM Globalization Pipeline](https://cloud.ibm.com/docs/services/GlobalizationPipeline).

IBM Globalization Pipeline is a DevOps integrated application translation management service that you can use to rapidly translate and release cloud and mobile applications to your global customers. Access IBM Globalization Pipeline capabilities through its dashboard, RESTful API, or integrate it seamlessly into your application's Delivery Pipeline.

This package expands on the [gettext module](https://docs.python.org/2/library/gettext.html) (avaliable as part of the Python standard library) and provides functionality for Python applications to use the Globalization Pipeline service.

Getting started
---------------
To get started, you should familiarize yourself with the service itself. A
good place to begin is by reading the [Quick Start Guide](https://github.com/IBM-Cloud/gp-common#quick-start-guide) and the official [Getting Started with IBM Globalization ](https://cloud.ibm.com/docs/services/GlobalizationPipeline) documentation.

The documentation explains how to find the service on IBM Cloud; authentication mechanisms supported; create a new service instance; create a new bundle; access the translated messages.

Demo
----
This [demo Bluemix app](http://gp-python-client-demo.mybluemix.net/) uses the Globalization Pipeline with the Python client to display a short welcome message that is translated in several languages. The source code for the demo app can be found in the [demo dir](./demo).

Installation
------------
To install `gp-python-client`, simply run:

```shell
$ pip install gp-python-client
```

Or if you're oldschool, run:

```shell
$ easy_install gp-python-client
```

API
---
The API documentation for the package can be found [here](http://pythonhosted.org/gp-python-client/). If the link is broken, you can [generate the documentation ](#generating-documentation) yourself.

Examples
--------
**Example 1 - Bluemix app:**

This sample code will allow you to get started using the Globalization Pipeline service in your Bluemix app. The example assumes the Bluemix app has been connected to a Globalization Pipeline service instance and has a bundle named `myBundle`, and that the bundle contains a source string with key `greet`.

```python
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
```

**Example 2 - Non-Bluemix app:**

This sample code will allow you to get started using the Globalization Pipeline service in a standalone Python app that is not hosted on Bluemix. The example assumes a Globalization Pipeline service instance exists with a bundle named `myBundle`, and that the bundle contains a source string with key `exit`.

You will need the [service instance credentials](https://github.com/IBM-Bluemix/gp-common#4-credentials).

```python
>>> from gpclient import GPClient, GPServiceAccount, GPTranslations
>>> import locale
>>>
>>> acc = GPServiceAccount(url=url, instanceId=instId,
    userId=userId, password=passwd) # Using Globalization Pipeline authentication
# Using IAM 
# acc = GPServiceAccount(url=url, instanceId=instanceId,
#                                apiKey=apiKey)
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
```

You can also provide the service credentials through a JSON file as shown in the snippet below

```python
>>> from gpclient import GPClient, GPServiceAccount
>>>
>>> acc = GPServiceAccount(credentialsJson="./local_credentials.json")
>>> client = GPClient(acc)
```

Obtaining language/locale codes
-------------------------------
This package requires that valid (BCP47 compliant) language/locale codes be provided when asked; for example, when calling `GPClient.translation()` (see [Examples](#examples)). From these codes, the language, region, and script subtags will be extracted.

Some example codes are:

* zh-Hans
* pt-BR
* ja
* en_US

There are several ways to get the code for the working locale. One way
is to use the [locale module](https://docs.python.org/2/library/locale.html) (avaliable as part of the Python standard library).

```python
>>> import locale
>>> myLocale = locale.getdefaultlocale()
>>> print myLocale
('en_US', 'UTF-8')
>>> code = myLocale[0]
>>> print code
en_US
```

For the above example, the language code is `en_US` - where `en` is the language subtag, and `US` is the region subtag.

Running Tests
-------------
Refer to [test/README.md](./test/README.md).

Generating documentation
------------------------
Documentation can be generated using [Sphinx](http://www.sphinx-doc.org).

You must first install it:

```shell
$ pip install sphinx
```

Then, to auto generate the documentation, run:

```shell
$ cd $BASEDIR/docs
$ make clean
$ make html
```

To navigate the documentation, open `$BASEDIR/docs/_build/html/index.html`.

Creating distribution package
-----------------------------
First update `CHANGES.txt` and `setup.py` if necessary (e.g. update version number), then create the preferred [distribution package](http://python-packaging-user-guide.readthedocs.org/en/latest/distributing/#packaging-your-project).

**Wheel distribution** (Recommended)

```shell
$ pip install wheel
$ python setup.py bdist_wheel
```

**Source distribution**

```shell
$ python setup.py sdist
```

Note: Source distribution contains tests as well.

**Build distribution**

```shell
$ python setup.py bdist
```

The new distribution files should be located under `$BASEDIR/dist/`.

Community
---------
* View or file GitHub [Issues](https://github.com/IBM-Cloud/gp-python-client/issues)
* Connect with the open source community on [developerWorks Open](https://developer.ibm.com/open/ibm-bluemix-globalization-pipeline-service/python-sdk/)

Contributing
------------
See [CONTRIBUTING.md](CONTRIBUTING.md).

License
-------
Apache 2.0. See [LICENSE.txt](LICENSE.txt).

> Licensed under the Apache License, Version 2.0 (the "License");
> you may not use this file except in compliance with the License.
> You may obtain a copy of the License at
>
> http://www.apache.org/licenses/LICENSE-2.0
>
> Unless required by applicable law or agreed to in writing, software
> distributed under the License is distributed on an "AS IS" BASIS,
> WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
> See the License for the specific language governing permissions and
> limitations under the License.
