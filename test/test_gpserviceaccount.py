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

import locale, gettext, unittest, datetime
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

    # @unittest.skip("skipping")
    def test_good_init(self):
        """Test the various valid ways to create a GPServiceAccount instance """

        # used to distinguish values for different GPServiceAccount init calls
        USER_KEY = 'userEnvVar'
        VCAP_KEY = 'vcap'

        common.set_user_env_vars(suffix=USER_KEY)
        common.set_vcap_env_vars(suffix=VCAP_KEY)

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

        # test init method with vcap env var
        common.unset_user_env_vars()
        acc = None
        acc = GPServiceAccount()
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

if __name__ == '__main__':
    unittest.main()
