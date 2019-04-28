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

import datetime
import unittest

from gpclient import GPClient
from test import common


@common.skipIfIamTestDisabled
class TestGPTranslationsIam(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        """Setting up the globalization pipeline for testing"""
        acc = common.get_admin_gpserviceaccount(True)
        client = GPClient(acc)
        try:
            client.delete_bundle(common.bundleId1)

            data = {}
            data['sourceLanguage'] = "en"
            # data['targetLanguages'] = ["fr","es-mx"]
            data['notes'] = ["string"]
            data['metadata'] = {}
            data['partner'] = ''
            data['segmentSeparatorPattern'] = 'string'
            data['noTranslationPattern'] = 'string'

            client.create_bundle(common.bundleId1, data=data)
            bundle1_entries = {}
            bundle1_entries['greet'] = "Hello"
            bundle1_entries['weather'] = "It is snowing"
            client.upload_resource_entries(common.bundleId1, "en", data=bundle1_entries)

            bundle2_entries = {}
            bundle2_entries['greet'] = "Salut"
            bundle2_entries['weather'] = "Il neige"
            client.upload_resource_entries(common.bundleId1, "fr", data=bundle2_entries)
            
        except:
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
    def test_caching_enabled_timeout_enabled(self):
        """Test when the caching feature in GPTranslations is enabled and
        there is a cache timeout
        """
        (t, _, key, tValue) = self.common_test_caching()

        # check that the cache map is as expected
        expectedCacheMap = {'greet': 'Salut', 'weather': "Il neige"}
        common.my_assert_equal(self, expectedCacheMap,
            t._GPTranslations__cachedMap, 'incorrect cache map')

        # modify the cachedMap and verify that the value is in fact obtained
        # from the cache and not directly from GP
        modifiedTValue = tValue + 'modified' # modified translated value
        t._GPTranslations__cachedMap[key] = modifiedTValue
        value = _(key)
        common.my_assert_equal(self, modifiedTValue, value,
            'incorrect translated value - should have returned cached value')

        # test cache is not expired one minute before timeout value
        oneMinBeforeTimeout = t._GPTranslations__cacheMapTimestamp - \
            datetime.timedelta(minutes=t._GPTranslations__cacheTimeout - 1)
        t._GPTranslations__cacheMapTimestamp = oneMinBeforeTimeout
        value = _(key)
        common.my_assert_equal(self, modifiedTValue, value,
            'incorrect translated value - should have returned cached value' +
            ' (time: cacheTimeout - 1)')

        # test cache is expired one minute after timeout value
        oneMinAfterTimeout =  t._GPTranslations__cacheMapTimestamp - \
            datetime.timedelta(minutes=t._GPTranslations__cacheTimeout + 1)
        t._GPTranslations__cacheMapTimestamp = oneMinAfterTimeout
        value = _(key)
        common.my_assert_equal(self, tValue, value,
            'incorrect translated value - should have returned non-cached' +
            ' value (time: cacheTimeout + 1)')

    # @unittest.skip("skipping")
    def test_caching_disabled(self):
        """Test when the caching feature in GPTranslations is disabled"""
        (t, _, key, tValue) = self.common_test_caching(
            cacheTimeout=0)

        # check that the cache map is empty
        expectedCacheMap = {}
        common.my_assert_equal(self, expectedCacheMap,
            t._GPTranslations__cachedMap, 'incorrect cache map')

    # @unittest.skip("skipping")
    def test_caching_enabled_timeout_disabled(self):
        """Test when the caching feature in GPTranslations is enabled and
        there is no cache timeout
        """
        (t, _, key, tValue) = self.common_test_caching(
            cacheTimeout=-1)

        # check that the cache map is as expected
        expectedCacheMap = {'greet': 'Salut', 'weather': "Il neige"}
        common.my_assert_equal(self, expectedCacheMap,
            t._GPTranslations__cachedMap, 'incorrect cache map')

        # modify the cachedMap and verify that the value is in fact obtained
        # from the cache and not directly from GP
        modifiedTValue = tValue + 'modified' # modified translated value
        t._GPTranslations__cachedMap[key] = modifiedTValue
        value = _(key)
        common.my_assert_equal(self, modifiedTValue, value,
            'incorrect translated value - should have returned cached value')

        # test cache is not expired 10 hours before timeout value
        tenHoursAfterTimeout =  t._GPTranslations__cacheMapTimestamp - \
            datetime.timedelta(hours=10)
        t._GPTranslations__cacheMapTimestamp = tenHoursAfterTimeout
        value = _(key)
        common.my_assert_equal(self, modifiedTValue, value,
            'incorrect translated value - should have returned cached value' +
            ' (no cache timeout)')

    def common_test_caching(self, cacheTimeout=None):
        """Shared code between the various caching tests """
        acc = common.get_gpserviceaccount(True)

        if cacheTimeout is None:
            client = GPClient(acc)
        else:
            client = GPClient(acc, cacheTimeout=cacheTimeout)

        languages=['fr_CA']
        t = client.gp_translation(bundleId=common.bundleId1,
            languages=languages)
        _ = t.gettext

        # key and translated value used for testing below
        # makes it easier to change
        key = 'greet'
        tValue = 'Salut' # translated value

        # check that the translated value is correct
        value = _(key)
        common.my_assert_equal(self, tValue, value,
            'incorrect translated value')

        return (t, _, key, tValue)

if __name__ == '__main__':
    unittest.main()
