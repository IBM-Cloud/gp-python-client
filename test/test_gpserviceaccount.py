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

import locale
import gettext
import unittest
import datetime
import os
from gpclient   import GPClient, GPServiceAccount, GPTranslations
from test       import common

class TestGPServiceAccount(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    @classmethod
    def tearDownClass(self):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        common.unset_user_env_vars()
        common.unset_vcap_env_vars()

    # @unittest.skip("skipping")
    def test_bad_init(self):
        """Test the various invalid ways to create a GPServiceAccount instance
        """
        with self.assertRaises(AssertionError):
            acc = GPServiceAccount()

    def test_good_init_gp_auth(self):
        """Test the various valid ways to create a GPServiceAccount instance using GP auth credentials """

        # used to distinguish values for different GPServiceAccount init calls
        USER_KEY = 'userEnvVarGp'
        VCAP_KEY = 'vcapGp'

        common.set_gp_auth_user_env_vars(suffix=USER_KEY)
        common.set_vcap_gp_auth_env_vars(suffix=VCAP_KEY)

        # test init method with params
        acc = common.get_gpserviceaccount()
        common.my_assert_equal(self, common.url, acc.get_url(),
                               'incorrect url from method params')
        common.my_assert_equal(self, common.instanceId, acc.get_instance_id(),
                               'incorrect instanceId from method params')
        common.my_assert_equal(self, common.userId, acc.get_user_id(),
                               'incorrect userId from method params')
        common.my_assert_equal(self, common.password, acc.get_password(),
                               'incorrect password from method params')
        common.my_assert_equal(self, False, acc.is_iam_enabled(),
                               'incorrect iam_enabled flag set when initialized with method params')

        # test init method with user defined env vars
        acc = GPServiceAccount()
        common.my_assert_equal(self, common.url + USER_KEY, acc.get_url(),
                               'incorrect url from user defined env vars')
        common.my_assert_equal(self, common.instanceId + USER_KEY,
                               acc.get_instance_id(),
                               'incorrect instanceId from user defined env vars')
        common.my_assert_equal(self, common.userId + USER_KEY,
                               acc.get_user_id(),
                               'incorrect userId from user defined env vars')
        common.my_assert_equal(self, common.password + USER_KEY,
                               acc.get_password(),
                               'incorrect password from user defined env vars')
        common.my_assert_equal(self, False, acc.is_iam_enabled(),
                               'incorrect iam_enabled flag set when initialized with env vars')

        # test init method with vcap env var
        common.unset_user_env_vars()
        acc = GPServiceAccount(serviceInstanceName=common.gpInstanceName)
        common.my_assert_equal(self, common.url + VCAP_KEY, acc.get_url(),
                               'incorrect url from vcap env var')
        common.my_assert_equal(self, common.instanceId + VCAP_KEY,
                               acc.get_instance_id(),
                               'incorrect instanceId from vcap env var')
        common.my_assert_equal(self, common.userId + VCAP_KEY,
                               acc.get_user_id(),
                               'incorrect userId from vcap env var')
        common.my_assert_equal(self, common.password + VCAP_KEY,
                               acc.get_password(),
                               'incorrect password from vcap env var')
        common.my_assert_equal(self, False, acc.is_iam_enabled(),
                               'incorrect iam_enabled flag set when initialized with vcap env var')

    def test_good_init_iam_auth(self):
        """Test the various valid ways to create a GPServiceAccount instance using IAM auth credentials"""

        # used to distinguish values for different GPServiceAccount init calls
        USER_KEY = 'userEnvVarIam'
        VCAP_KEY = 'vcapIam'

        common.set_iam_env_vars(suffix=USER_KEY)
        common.set_vcap_iam_auth_env_vars(suffix=VCAP_KEY)

        # test init method with params
        acc = common.get_gpserviceaccount(True)
        common.my_assert_equal(self, common.url, acc.get_url(),
                               'incorrect url from method params')
        common.my_assert_equal(self, common.instanceId, acc.get_instance_id(),
                               'incorrect instanceId from method params')
        common.my_assert_equal(self, common.apiKey, acc.get_api_key(),
                               'incorrect apiKey from method params')
        common.my_assert_equal(self, True, acc.is_iam_enabled(),
                               'incorrect iam_enabled flag set when initialized with method params')


        # test init method with user defined env vars
        acc = GPServiceAccount()
        common.my_assert_equal(self, common.url + USER_KEY, acc.get_url(),
                               'incorrect url from user defined env vars')
        common.my_assert_equal(self, common.instanceId + USER_KEY,
                               acc.get_instance_id(),
                               'incorrect instanceId from user defined env vars')
        common.my_assert_equal(self, common.apiKey + USER_KEY, acc.get_api_key(),
                               'incorrect apiKey from user defined env vars')
        common.my_assert_equal(self, True, acc.is_iam_enabled(),
                               'incorrect iam_enabled flag set when initialized with env vars')

        # test init method with vcap env var
        common.unset_user_env_vars()
        acc = GPServiceAccount(serviceInstanceName=common.gpInstanceName)
        common.my_assert_equal(self, common.url + VCAP_KEY, acc.get_url(),
                               'incorrect url from vcap env var')
        common.my_assert_equal(self, common.instanceId + VCAP_KEY,
                               acc.get_instance_id(),
                               'incorrect instanceId from vcap env var')
        common.my_assert_equal(self, common.apiKey + VCAP_KEY, acc.get_api_key(),
                               'incorrect apiKey from vcap env var')
        common.my_assert_equal(self, True, acc.is_iam_enabled(),
                               'incorrect iam_enabled flag set when initialized with vcap env var')


    # @unittest.skip("skipping")
    def test_good_init(self):
        """Test the various valid ways to create a GPServiceAccount instance when both GP and IAM env variables are present"""

        # used to distinguish values for different GPServiceAccount init calls
        USER_KEY = 'userEnvVar'
        VCAP_KEY = 'vcap'

        common.set_all_auth_user_env_vars(suffix=USER_KEY)
        common.set_vcap_gp_auth_env_vars(suffix=VCAP_KEY)

        # test init method with params
        acc = common.get_gpserviceaccount()
        common.my_assert_equal(self, common.url, acc.get_url(),
            'incorrect url from method params')
        common.my_assert_equal(self, common.instanceId, acc.get_instance_id(),
            'incorrect instanceId from method params')
        common.my_assert_equal(self, common.userId, acc.get_user_id(),
            'incorrect userId from method params')
        common.my_assert_equal(self, common.password, acc.get_password(),
            'incorrect password from method params')
        common.my_assert_equal(self, False, acc.is_iam_enabled(),
                               'incorrect iam_enabled flag set when initialized with method params')


        # test init method with user defined env vars
        acc = GPServiceAccount()
        common.my_assert_equal(self, common.url + USER_KEY, acc.get_url(),
            'incorrect url from user defined env vars')
        common.my_assert_equal(self, common.instanceId + USER_KEY,
            acc.get_instance_id(),
            'incorrect instanceId from user defined env vars')
        common.my_assert_equal(self, common.userId + USER_KEY,
            acc.get_user_id(),
            'incorrect userId from user defined env vars')
        common.my_assert_equal(self, common.password + USER_KEY,
            acc.get_password(),
            'incorrect password from user defined env vars')
        common.my_assert_equal(self, False, acc.is_iam_enabled(),
                               'incorrect iam_enabled flag set when initialized with env vars')

        # test init method with vcap env var
        common.unset_user_env_vars()
        acc = GPServiceAccount(serviceInstanceName=common.gpInstanceName)
        common.my_assert_equal(self, common.url + VCAP_KEY, acc.get_url(),
            'incorrect url from vcap env var')
        common.my_assert_equal(self, common.instanceId + VCAP_KEY,
            acc.get_instance_id(),
            'incorrect instanceId from vcap env var')
        common.my_assert_equal(self, common.userId + VCAP_KEY,
            acc.get_user_id(),
            'incorrect userId from vcap env var')
        common.my_assert_equal(self, common.password + VCAP_KEY,
            acc.get_password(),
            'incorrect password from vcap env var')
        common.my_assert_equal(self, False, acc.is_iam_enabled(),
                               'incorrect iam_enabled flag set when initialized with vcap env var')
        
    # @unittest.skip("skipping")
    def test_loadCredentialsFromFile(self):
        """Test to support loading credentials from json file"""
        acc = GPServiceAccount(credentialsJson="test/data/local-credentials.json")
        
if __name__ == '__main__':
    unittest.main()
