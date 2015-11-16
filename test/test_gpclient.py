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

class TestGPClient(unittest.TestCase):

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
    def test_example_1(self):
        """Test example 1 used in the docs"""
        common.set_vcap_env_vars()

        acc = GPServiceAccount()
        client = GPClient(acc)

        languages=['fr_CA'] # languages=[locale.getdefaultlocale()[0]]

        t = client.gp_translation(bundleId=common.bundleId1,
            languages=languages)
        _ = t.gettext

        value = _('greet') # 'greet' key will be localized/translated to French

        common.my_assert_equal(self, 'Bonjour', value,
            'incorrect translated value')

    # @unittest.skip("skipping")
    def test_example_2(self):
        """Test example 2 used in the docs"""
        acc = common.get_gpserviceaccount()
        client = GPClient(acc)

        languages=['es-mx'] # languages=[locale.getdefaultlocale()[0]]

        t = client.gp_translation(bundleId=common.bundleId2,
            languages=languages)
        _ = t.gettext

        value = _('exit') # 'exit' key will be localized/translated to Spanish

        common.my_assert_equal(self, u'Adiós', value,
            'incorrect translated value')

    # @unittest.skip("skipping")
    def test_gp_fallback(self):
        """Test the fallback feature, i.e. when a translated value is not found
        for a language, the fallback language should be used - if there is no
        fallback language then the source value should be returned.

        If the key is not found, the key should be returned.
        """
        acc = common.get_gpserviceaccount()
        client = GPClient(acc)

        # should fallbcak to 'es-mx', 'ur' is not supported
        languages=['ur', 'es-mx', 'fr']
        t = client.gp_translation(bundleId=common.bundleId2,
            languages=languages)
        _ = t.gettext
        value = _('exit')

        common.my_assert_equal(self, u'Adiós', value,
            'incorrect translated value - should have used es-mx fallback')

        # should return key back, key doesn't exist
        languages=['es-mx']
        t = client.gp_translation(bundleId=common.bundleId2,
            languages=languages)
        _ = t.gettext
        key = 'badKey'
        value = _(key)

        common.my_assert_equal(self, key, value,
            'incorrect translated value - key doesn\'t exist')

    # @unittest.skip("skipping")
    def test_get_gaas_hmac_headers(self):
        """Test if the GaaS HMAC header generation is correct """
        method = 'POST'
        url = 'https://example.com/gaas'
        date = 'Mon, 30 Jun 2014 00:00:00 GMT'
        body = '{"param":"value"}'

        userId = 'MyUser'
        secret = 'MySecret'

        expectedHeaders = {'Date': 'Mon, 30 Jun 2014 00:00:00 GMT',
            'Authorization': 'GaaS-HMAC MyUser:ONBJapYEveDZfsPFdqZHQ64GDgc='}

        acc = common.get_gpserviceaccount()
        client = GPClient(acc)

        headers = client._GPClient__get_gaas_hmac_headers(  method=method,
            url=url, date=date, body=body, secret=secret, userId=userId)

        common.my_assert_equal(self, expectedHeaders, headers,
            'incorrect GaaS HMAC headers')

    # @unittest.skip("skipping")
    def test_get_language_match(self):
        """Test the matching of langauge codes to supported langauges"""
        # supported languages in GP
        supportedLangs = ['en','de','es','fr','it', 'ja','ko', 'pt-BR',
            'zh-Hans', 'zh-Hant']

        acc = common.get_gpserviceaccount()
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

    # @unittest.skip("skipping")
    def test_basic_auth_translation(self):
        """Test if translation works with basic auth"""
        acc = common.get_gpserviceaccount()
        client = GPClient(acc, auth=GPClient.BASIC_AUTH)

        languages=['es-mx']

        t = client.gp_translation(bundleId=common.bundleId2,
            languages=languages)
        _ = t.gettext

        value = _('show')

        common.my_assert_equal(self, u'El físico', value,
            'incorrect translated value')

    # @unittest.skip("skipping")
    def test_reader__get_bundles(self):
        """Verify bundles can not be obtained with reader acc"""
        acc = common.get_gpserviceaccount()
        client = GPClient(acc)

        expectedBundles = None
        actualBundles = client._GPClient__get_bundles_data()

        common.my_assert_equal(self, expectedBundles, actualBundles,
            'reader acc can not get bundles list')

    # @unittest.skip("skipping")
    def test_admin_basic_auth(self):
        """Verify basic auth fails with admin account"""
        acc = common.get_admin_gpserviceaccount()
        client = GPClient(acc, auth=GPClient.BASIC_AUTH)

        languages=['es-mx']

        t = client.gp_translation(bundleId=common.bundleId2,
            languages=languages)
        _ = t.gettext

        value = _('show')

        common.my_assert_equal(self, 'show', value,
            'admin acc can not use basic auth')

    # @unittest.skip("skipping")
    def test_english_values(self):
        """Verify English values are returned when asked for"""
        acc = common.get_gpserviceaccount()
        client = GPClient(acc)

        languages=['en']

        t = client.gp_translation(bundleId=common.bundleId1,
            languages=languages)
        _ = t.gettext

        value = _('greet')

        common.my_assert_equal(self, 'Hello', value,
            'incorrect value')

    # @unittest.skip("skipping")
    def test_local_translations(self):
        """Verify local translations are used with expected"""
        acc = common.get_gpserviceaccount()
        client = GPClient(acc)

        languages=['fr']

        t = client.translation(bundleId=common.bundleId1,
            languages=languages, priority='local', domain='messages',
            localedir='test/data/translations', class_=None, codeset=None)
        _ = t.gettext

        value = _('greet')

        common.my_assert_equal(self, 'greet in French (local)', value,
            'incorrect value; should have returned local translation')

    # @unittest.skip("skipping")
    def test_translation_priority(self):
        """Verify that the priority option in GPClient.translation works"""
        acc = common.get_gpserviceaccount()
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

        common.my_assert_equal(self, 'Bonjour', value,
            'incorrect value; should have returned gp translation')

    # @unittest.skip("skipping")
    def test_local_fallback(self):
        """Verify local translations are used with expected"""
        acc = common.get_gpserviceaccount()
        client = GPClient(acc)

        languages=['fo', 'fr']

        t = client.translation(bundleId=common.bundleId1,
            languages=languages, priority='local', domain='messages',
            localedir='test/data/translations', class_=None, codeset=None)
        _ = t.gettext

        value = _('greet')

        common.my_assert_equal(self, 'greet in French (local)', value,
            'incorrect value; should have returned local translation')

if __name__ == '__main__':
    unittest.main()
