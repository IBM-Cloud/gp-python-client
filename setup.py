from setuptools import setup, find_packages
from codecs import open
from os import path

currentDir = path.abspath(path.dirname(__file__))

with open(path.join(currentDir, 'README.md'), encoding='utf-8') as readme:
    long_description = readme.read()

setup(
    name='gp-python-client',
    version='1.1.2',
    description='Python client for Globalization Pipeline on IBM Cloud',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/IBM-Cloud/gp-python-client',
    author='Farhan Arshad',
    author_email='icuintl@us.ibm.com',
    license='Apache License Version 2.0',
    keywords='client globalization pipline ibm bluemix',
    packages=['gpclient'],
    install_requires=["requests", "babel", "dateutils"],
    test_suite="test",

    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Localization',

        'License :: OSI Approved :: Apache Software License',

        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ]

)
