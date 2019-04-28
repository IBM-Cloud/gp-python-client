# -*- coding: utf-8 -*-

# Copyright IBM Corp. 2015, 2017
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

import json
import logging
import os
import unittest

from gpclient import GPServiceAccount, GPClient


def __get_reader_credentials():
    acc = GPServiceAccount(url=url, instanceId=instanceId,
                           userId=adminUserId, password=adminPassword)
    client = GPClient(acc)
    return client.createReaderUser(['*'])

try:
    iamTestEnabled = os.environ['IAM_TEST_DISABLED']
    url = os.environ['GP_URL']
    adminUserId = os.environ['GP_ADMIN_USER']
    adminPassword = os.environ['GP_ADMIN_PASS']
    userId = os.environ['GP_READER_USER']
    password = os.environ['GP_READER_PASS']
    instanceId = os.environ['GP_INSTANCE_ID']
    gpInstanceName = os.environ['GP_INSTANCE_NAME']
    apiKey = os.environ['GP_IAM_API_KEY']
    adminApiKey = os.environ['GP_ADMIN_IAM_API_KEY']
except:
    try:
        logging.warning('Failed to initialize with env var. '
                        'Trying to initialize with ./local-credentials.json')
        with open('./local-credentials.json') as credsFile:
            credsData = json.load(credsFile)
            creds = credsData.get('credentials')
            url = creds.get('url')
            instanceId = creds.get('instanceId')
            # admin acc
            adminUserId = creds.get('userId')
            adminPassword = creds.get('password')
            # reader acc
            c=__get_reader_credentials()
            userId= c['user']['id']
            password = c['user']['password']
            # reader acc
            #apiKey = creds.get('readerApiKey')
            # admin acc
            #adminApiKey = creds.get('adminApiKey')
            gpInstanceName = creds.get("gp-instance-name")
            apiKey = 'DUMMY_API_KEY'
            # admin acc
            adminApiKey= 'DUMMY_ADMIN_API_KEY'
            if not gpInstanceName:
                gpInstanceName = 'test-instance-name'
    except:
        logging.warning('Failed to initialize with ./local-credentials.json '
                        'Trying to initialize with test/data/creds.json')
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
            # reader acc
            apiKey = creds.get('readerApiKey')
            # admin acc
            adminApiKey= creds.get('adminApiKey')
            gpInstanceName = creds.get("gp-instance-name")
    
# bundles in the test service
bundleId1 = "gpclient-test-1"
bundleId2 = "gpclient-test-2"

skipIfIamTestDisabled = unittest.skipIf(
    'True' == os.environ.get('IAM_TEST_DISABLED', 'True'), 'IAM tests disabled. Set IAM_TEST_DISABLED=False to run them.')

def get_gpserviceaccount(iamEnabled=False):
    if iamEnabled:
        acc = GPServiceAccount(url=url, instanceId=instanceId,
                                apiKey=apiKey)
    else:
        acc = GPServiceAccount(url=url, instanceId=instanceId,
                           userId=userId, password=password, serviceInstanceName=None, credentialsJson=None, apiKey=apiKey)
    return acc

def get_admin_gpserviceaccount(iamEnabled=False):
    if iamEnabled:
        acc = GPServiceAccount(url=url, instanceId=instanceId,
                               apiKey=adminApiKey)
    else:
        acc = GPServiceAccount(url=url, instanceId=instanceId,
                               userId=adminUserId, password=adminPassword,
                               serviceInstanceName=None, credentialsJson=None, apiKey=adminApiKey)
    return acc

def my_assert_equal(test, expected, actual, message=''):
    message += (' <Expected= "%s", Actual= "%s">' % (expected, actual))
    # print message
    test.assertEqual(expected, actual, message)

def set_user_env_vars(suffix=None):
    """Set user defined environment variables for both GP and IAM auth"""
    os.environ[GPServiceAccount.GP_URL_ENV_VAR] = url+str(suffix)
    os.environ[GPServiceAccount.GP_INSTANCE_ID_ENV_VAR] = \
        instanceId+str(suffix)
    os.environ[GPServiceAccount.GP_USER_ID_ENV_VAR] = \
        userId+str(suffix)
    os.environ[GPServiceAccount.GP_PASSWORD_ENV_VAR] = \
        password+str(suffix)
    os.environ[GPServiceAccount.GP_IAM_API_KEY_ENV_VAR] = \
        apiKey + str(suffix)

def set_all_auth_user_env_vars(suffix=None):
    """Set user defined environment variables for both GP and IAM auth"""
    os.environ[GPServiceAccount.GP_URL_ENV_VAR] = url+str(suffix)
    os.environ[GPServiceAccount.GP_INSTANCE_ID_ENV_VAR] = \
        instanceId+str(suffix)
    os.environ[GPServiceAccount.GP_USER_ID_ENV_VAR] = \
        userId+str(suffix)
    os.environ[GPServiceAccount.GP_PASSWORD_ENV_VAR] = \
        password+str(suffix)
    os.environ[GPServiceAccount.GP_IAM_API_KEY_ENV_VAR] = \
        apiKey + str(suffix)

def set_gp_auth_user_env_vars(suffix=None):
    """Set user defined environment variables for GP auth"""
    os.environ[GPServiceAccount.GP_URL_ENV_VAR] = url+str(suffix)
    os.environ[GPServiceAccount.GP_INSTANCE_ID_ENV_VAR] = \
        instanceId+str(suffix)
    os.environ[GPServiceAccount.GP_USER_ID_ENV_VAR] = \
        userId+str(suffix)
    os.environ[GPServiceAccount.GP_PASSWORD_ENV_VAR] = \
        password+str(suffix)


def set_iam_env_vars(suffix=None):
    """Set user defined environment variables for IAM auth"""
    os.environ[GPServiceAccount.GP_URL_ENV_VAR] = url+str(suffix)
    os.environ[GPServiceAccount.GP_INSTANCE_ID_ENV_VAR] = \
        instanceId+str(suffix)
    os.environ[GPServiceAccount.GP_IAM_API_KEY_ENV_VAR] = \
        apiKey + str(suffix)

def unset_user_env_vars():
    """Unset user defined environment variables for both GP and IAM auth"""
    if os.environ.get(GPServiceAccount.GP_URL_ENV_VAR):
        del os.environ[GPServiceAccount.GP_URL_ENV_VAR]

    if os.environ.get(GPServiceAccount.GP_INSTANCE_ID_ENV_VAR):
        del os.environ[GPServiceAccount.GP_INSTANCE_ID_ENV_VAR]

    if os.environ.get(GPServiceAccount.GP_USER_ID_ENV_VAR):
        del os.environ[GPServiceAccount.GP_USER_ID_ENV_VAR]

    if os.environ.get(GPServiceAccount.GP_PASSWORD_ENV_VAR):
        del os.environ[GPServiceAccount.GP_PASSWORD_ENV_VAR]

    if os.environ.get(GPServiceAccount.GP_IAM_API_KEY_ENV_VAR):
        del os.environ[GPServiceAccount.GP_IAM_API_KEY_ENV_VAR]

def set_vcap_gp_auth_env_vars(suffix=None):
    """Set VCAP_SERVICES environment variable -
    simulates the VCAP_SERVICES env var found when running through Bluemix
    """
    ## the value should look like this for GP auth:
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
    credsData["apikey"] = apiKey + suffix if suffix else apiKey

    serviceData = {}
    # instance name
    serviceData["name"] = gpInstanceName
    serviceData["label"] = "gp-beta" # label
    serviceData["plan"] = "gp-beta-plan" # plan
    serviceData["credentials"] = credsData

    data = {}
    data["gp-beta"] =[serviceData] # service name
    json_data = json.dumps(data)
    os.environ[GPServiceAccount._GPServiceAccount__VCAP_SERVICES_ENV_VAR] = \
        json_data

def set_vcap_iam_auth_env_vars(suffix=None):
    """Set VCAP_SERVICES environment variable -
    simulates the VCAP_SERVICES env var found when running through Bluemix

    ## the value should look like this for IAM auth:
    #     {
    #         "service name": [
    #           {
    #              "name": "service instance name",
    #              "label": "label",
    #              "plan": "plan",
    #              "credentials": {
    #                 "url": "url",
    #                 "apikey": "userId",
    #                 "iam_endpoint": "iam_endpoint",
    #                 "instanceId": "instanceId"
    #              }
    #           }
    #         ]
    #     }
    # """

    credsData = {}
    credsData["url"] = url + suffix if suffix else url
    credsData["instanceId"] = instanceId + suffix if suffix else instanceId
    credsData["apikey"] = apiKey + suffix if suffix else apiKey

    serviceData = {}
    # instance name
    serviceData["name"] = gpInstanceName
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
