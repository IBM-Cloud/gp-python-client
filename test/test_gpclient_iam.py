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

import unittest

from gpclient import GPClient
from test import common


@common.skipIfIamTestDisabled
class TestGPClientIam(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        """Setting up the globalization pipeline for testing"""
        acc = common.get_admin_gpserviceaccount(True)
        client = GPClient(acc)
        try:
            client.delete_bundle(common.bundleId1)
            client.delete_bundle(common.bundleId2)

            data = {}
            data['sourceLanguage'] = "en"
            # data['targetLanguages'] = ["fr","es-mx"]
            data['targetLanguages'] = []
            data['notes'] = ["string"]
            data['metadata'] = {}
            data['partner'] = ''
            data['segmentSeparatorPattern'] = 'string'
            data['noTranslationPattern'] = 'string'

            client.create_bundle(common.bundleId1, data=data)
            bundle_entries = {}
            bundle_entries['greet'] = "Hello"
            bundle_entries['weather'] = "It is snowing"
            client.upload_resource_entries(common.bundleId1, "en", data=bundle_entries)

            bundle1_entries = {}
            bundle1_entries['greet'] = "Salut"
            bundle1_entries['weather'] = "Il neige"
            client.upload_resource_entries(common.bundleId1, "fr", data=bundle1_entries)

            bundle3_entries = {}
            bundle3_entries['greet'] = "Salut"
            bundle3_entries['weather'] = "Il neige"
            client.upload_resource_entries(common.bundleId1, "es-mx", data=bundle3_entries)

            client.create_bundle(common.bundleId2, data=data)
            bundle0_entries = {}
            bundle0_entries['exit'] = "Goodbye"
            bundle0_entries['show'] = "The Wire"
            client.upload_resource_entries(common.bundleId2, "en", data=bundle0_entries)

            bundle2_entries = {}
            bundle2_entries['exit'] = u'Au revoir'
            bundle2_entries['show'] = u'Le Fil'
            client.upload_resource_entries(common.bundleId2, "fr", data=bundle2_entries)
        except:
            pass

    @classmethod
    def tearDownClass(self):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    #@unittest.skip("skipping")
    def test_translation(self):
        """Test if translation works with basic auth"""
        acc = common.get_gpserviceaccount(True)
        client = GPClient(acc)

        languages=['fr']

        t = client.gp_translation(bundleId=common.bundleId2,
            languages=languages)
        _ = t.gettext

        value = _('show')

        common.my_assert_equal(self, u'Le Fil', value,
            'incorrect translated value')
    
    #@unittest.skip("skipping")
    def test_create_bundle(self):
        """Test to create a new bundle"""
        acc = common.get_admin_gpserviceaccount(True)
        client = GPClient(acc)
        
        tresp = client.create_bundle("test-bundle")
        
        common.my_assert_equal(self, "SUCCESS", tresp["status"],
            'bundle could not be created')
    
    #@unittest.skip("skipping")
    def test_delete_bundle_fail(self):
        """Test to delete a specific bundle which doesn't exist"""
        acc = common.get_admin_gpserviceaccount(True)
        client = GPClient(acc)
        
        tresp = client.delete_bundle("test-bundle-notexists")
        
        common.my_assert_equal(self, "SUCCESS", tresp["status"],
            'a bundle which does not exist can not be deleted')
    
    #@unittest.skip("skipping")
    def test_delete_bundle_success(self):
        """Test to delete a specific bundle which exists"""
        acc = common.get_admin_gpserviceaccount(True)
        client = GPClient(acc)
        
        tresp = client.delete_bundle("test-bundle")
        
        common.my_assert_equal(self, "SUCCESS", tresp["status"],
            'bundle could not be deleted')
        
    #@unittest.skip("skipping")
    def test_english_values(self):
        """Verify English values are returned when asked for"""
        acc = common.get_gpserviceaccount(True)
        client = GPClient(acc)

        languages=['en']

        t = client.gp_translation(bundleId=common.bundleId1,
            languages=languages)
        _ = t.gettext

        value = _('greet')

        common.my_assert_equal(self, 'Hello', value,
            'incorrect value')
        
    #@unittest.skip("skipping")
    def test_example_1(self):
        """Test example 1 used in the docs"""
        #common.set_vcap_env_vars()

        acc = common.get_gpserviceaccount(True)
        client = GPClient(acc)

        languages=['fr'] # languages=[locale.getdefaultlocale()[0]]

        t = client.gp_translation(bundleId=common.bundleId1,
            languages=languages)
        _ = t.gettext

        value = _('greet') # 'greet' key will be localized/translated to French

        common.my_assert_equal(self, 'Salut', value,
            'incorrect translated value')

    #@unittest.skip("skipping")
    def test_example_2(self):
        """Test example 2 used in the docs"""
        acc = common.get_gpserviceaccount(True)
        client = GPClient(acc)

        languages=['fr'] # languages=[locale.getdefaultlocale()[0]]

        t = client.gp_translation(bundleId=common.bundleId2,
            languages=languages)
        _ = t.gettext

        value = _('exit') # 'exit' key will be localized/translated to French

        common.my_assert_equal(self, u'Au revoir', value,
            'incorrect translated value')
        
    #@unittest.skip("skipping")
    def test_get_language_match(self):
        """Test the matching of langauge codes to supported langauges"""
        # supported languages in GP
        supportedLangs = ['en','de','es','fr','it', 'ja','ko', 'pt-BR',
            'zh-Hans', 'zh-Hant']

        acc = common.get_gpserviceaccount(True)
        client = GPClient(acc)
        get_language_match = client._GPClient__get_language_match

        expectedMatches = {
            'en': 'en', 'en_US': 'en', 'en-US': 'en',
            'de': 'de', 'de_at': 'de', 'de-at': 'de',
            'es': 'es', 'es_mx': 'es', 'es-mx': 'es',
            'fr': 'fr', 'fr_FR': 'fr', 'fr-Fr': 'fr', 'fr_CA': 'fr',
            'it': 'it', 'it_ch': 'it', 'it-ch': 'it', 'it-IT': 'it',
            'ja': 'ja', 'ja_JA': 'ja', 'ja-JA': 'ja',
            'ko': 'ko', 'ko_KO': 'ko', 'ko-KO': 'ko',
            'pt-BR': 'pt-BR', 'pt': None,
            'zh': 'zh-Hans', 'zh-tw': 'zh-Hant', 'zh-cn': 'zh-Hans',
            'zh-hk': 'zh-Hant', 'zh-sg': 'zh-Hans',
            }

        for langCode in expectedMatches:
            match = get_language_match(langCode, supportedLangs)
            expectedMatch  = expectedMatches[langCode]
            common.my_assert_equal(self, expectedMatch, match,
                'incorrect langauge match (Input= %s)' % (langCode,))

    #@unittest.skip("skipping")
    def test_gp_fallback(self):
        """Test the fallback feature, i.e. when a translated value is not found
        for a language, the fallback language should be used - if there is no
        fallback language then the source value should be returned.

        If the key is not found, the key should be returned.
        """
        acc = common.get_gpserviceaccount(True)
        client = GPClient(acc)

        # should fallbcak to 'fr', 'ur' is not supported
        languages=['ur', 'fr']
        t = client.gp_translation(bundleId=common.bundleId2,
            languages=languages)
        _ = t.gettext
        value = _('exit')

        common.my_assert_equal(self, u'Au revoir', value,
            'incorrect translated value - should have used fr fallback')

        # should return key back, key doesn't exist
        languages=['es-mx']
        t = client.gp_translation(bundleId=common.bundleId2,
            languages=languages)
        _ = t.gettext
        key = 'badKey'
        value = _(key)

        common.my_assert_equal(self, key, value,
            'incorrect translated value - key doesn\'t exist')
        
    #@unittest.skip("skipping")
    def test_local_fallback(self):
        """Verify local translations are used with expected"""
        acc = common.get_gpserviceaccount(True)
        client = GPClient(acc)

        languages=['fo', 'fr']

        t = client.translation(bundleId=common.bundleId1,
            languages=languages, priority='local', domain='messages',
            localedir='test/data/translations', class_=None, codeset=None)
        _ = t.gettext

        value = _('greet')

        common.my_assert_equal(self, 'greet in French (local)', value,
            'incorrect value; should have returned local translation')
        
    #@unittest.skip("skipping")
    def test_local_translations(self):
        """Verify local translations are used with expected"""
        acc = common.get_gpserviceaccount(True)
        client = GPClient(acc)

        languages=['fr']

        t = client.translation(bundleId=common.bundleId1,
            languages=languages, priority='local', domain='messages',
            localedir='test/data/translations', class_=None, codeset=None)
        _ = t.gettext

        value = _('greet')

        common.my_assert_equal(self, 'greet in French (local)', value,
            'incorrect value; should have returned local translation')

    #@unittest.skip("skipping")
    def test_reader_get_bundles(self):
        """Verify bundles can not be obtained with reader acc"""
        acc = common.get_gpserviceaccount(True)
        client = GPClient(acc)

        expectedBundles = []
        actualBundles = client.get_bundles()

        common.my_assert_equal(self, expectedBundles, actualBundles,
            'reader acc can not get bundles list')

    
    #@unittest.skip("skipping")
    def test_translation_priority(self):
        """Verify that the priority option in GPClient.translation works"""
        acc = common.get_gpserviceaccount(True)
        client = GPClient(acc)

        languages=['fr']

        # prioritize local
        t = client.translation(bundleId=common.bundleId1,
            languages=languages, priority='local', domain='messages',
            localedir='test/data/translations', class_=None, codeset=None)
        _ = t.gettext

        value = _('greet')

        common.my_assert_equal(self, 'greet in French (local)', value,
            'incorrect value; should have returned local translation')

        # prioritize gp
        t = client.translation(bundleId=common.bundleId1,
            languages=languages, priority='gp', domain='messages',
            localedir='test/data/translations', class_=None, codeset=None)
        _ = t.gettext

        value = _('greet')

        common.my_assert_equal(self, 'Salut', value,
            'incorrect value; should have returned gp translation')

    #@unittest.skip("skipping")
    def test_update_resource_entry(self):
        """Test to update a resource entry"""
        acc = common.get_admin_gpserviceaccount(True)
        client = GPClient(acc)
        data = {}
        data['value'] = "weather in spanish"
        tresp = client.update_resource_entry(common.bundleId1,"es-mx","weather", data=data)
        common.my_assert_equal(self, "SUCCESS", tresp["status"],
            'bundle resource entry for the language could not be updated')
    
    #@unittest.skip("skipping")
    def test_update_resource_entries(self):
        """Test to update resource entries"""
        acc = common.get_admin_gpserviceaccount(True)
        client = GPClient(acc)
        data = {}
        data["welcome"]="Welcome"
        tresp = client.update_resource_entries(common.bundleId1,"en", data=data)
        common.my_assert_equal(self, "SUCCESS", tresp["status"],
            'bundle resource entries for the language could not be updated')
        
    #@unittest.skip("skipping")
    def test_upload_resource_entries(self):
        """Test to upload resource entries"""
        acc = common.get_admin_gpserviceaccount(True)
        client = GPClient(acc)
        data = {}
        data["welcome"]="Hello"
        tresp = client.upload_resource_entries(common.bundleId1,"en", data=data)
        common.my_assert_equal(self, "SUCCESS", tresp["status"],
            'bundle resource entries could not be uploaded')
    
if __name__ == '__main__':
    unittest.main()
