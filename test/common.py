# -*- coding: utf-8 -*-

# Copyright IBM Corp. 2015
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os, locale, json, gettext, datetime
from gpclient import GPClient, GPServiceAccount, GPTranslations

with open('test/data/creds.json') as credsFile:
    credsData = json.load(credsFile)
    creds = credsData.get('credentials')

url = creds.get('url')
instanceId= creds.get('instanceId')

# admin acc
adminUserId = creds.get('userId')
adminPassword = creds.get('password')

# reader acc
userId = creds.get('readerUserId')
password = creds.get('readerPassword')

# bundles in the test service
bundleId1 = "gpclient-test-1"
bundleId2 = "gpclient-test-2"

def get_gpserviceaccount():
    acc = GPServiceAccount(url=url, instanceId=instanceId,
        userId=userId, password=password)
    return acc

def get_admin_gpserviceaccount():
    acc = GPServiceAccount(url=url, instanceId=instanceId,
        userId=adminUserId, password=adminPassword)
    return acc

def my_assert_equal(test, expected, actual, message=''):
    message += (' <Expected= "%s", Actual= "%s">' % (expected, actual))
    # print message
    test.assertEqual(expected, actual, message)

def set_user_env_vars(suffix=None):
    """Set user defined environment variables """
    os.environ[GPServiceAccount.GP_URL_ENV_VAR] = url + suffix
    os.environ[GPServiceAccount.GP_INSTANCE_ID_ENV_VAR] = \
        instanceId + suffix
    os.environ[GPServiceAccount.GP_USER_ID_ENV_VAR] = \
        userId + suffix
    os.environ[GPServiceAccount.GP_PASSWORD_ENV_VAR] = \
        password + suffix

def unset_user_env_vars():
    """Unset user defined environment variables """
    if os.environ.get(GPServiceAccount.GP_URL_ENV_VAR):
        del os.environ[GPServiceAccount.GP_URL_ENV_VAR]

    if os.environ.get(GPServiceAccount.GP_INSTANCE_ID_ENV_VAR):
        del os.environ[GPServiceAccount.GP_INSTANCE_ID_ENV_VAR]

    if os.environ.get(GPServiceAccount.GP_USER_ID_ENV_VAR):
        del os.environ[GPServiceAccount.GP_USER_ID_ENV_VAR]

    if os.environ.get(GPServiceAccount.GP_PASSWORD_ENV_VAR):
        del os.environ[GPServiceAccount.GP_PASSWORD_ENV_VAR]

def set_vcap_env_vars(suffix=None):
    """Set VCAP_SERVICES environment variable -
    simulates the VCAP_SERVICES env var found when running through Bluemix
    """
    ## the value should look like this:
    #     {
    #         "service name": [
    #           {
    #              "name": "service instance name",
    #              "label": "label",
    #              "plan": "plan",
    #              "credentials": {
    #                 "url": "url",
    #                 "userId": "userId",
    #                 "password": "password",
    #                 "instanceId": "instanceId"
    #              }
    #           }
    #         ]
    #     }
    # """

    credsData = {}
    credsData["url"] = url + suffix if suffix else url
    credsData["userId"] = userId + suffix if suffix else userId
    credsData["password"] = password + suffix if suffix else password
    credsData["instanceId"] = instanceId + suffix if suffix else instanceId

    serviceData = {}
    # instance name
    serviceData["name"] = "Globalization Pipeline DEV-py-client-test"
    serviceData["label"] = "gp-beta" # label
    serviceData["plan"] = "gp-beta-plan" # plan
    serviceData["credentials"] = credsData

    data = {}
    data["gp-beta"] =[serviceData] # service name
    json_data = json.dumps(data)
    os.environ[GPServiceAccount._GPServiceAccount__VCAP_SERVICES_ENV_VAR] = \
        json_data

def unset_vcap_env_vars():
    """Unset VCAP_SERVICES environment variable"""
    vcapEnvVarKey = GPServiceAccount._GPServiceAccount__VCAP_SERVICES_ENV_VAR
    if os.environ.get(vcapEnvVarKey):
        del os.environ[vcapEnvVarKey]
