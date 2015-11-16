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

import datetime
from gettext import NullTranslations

class GPTranslations(NullTranslations):
    """``GPTranslations`` extends `gettext.NullTranslations
    <https://docs.python.org/2/library/gettext.html#gettext.NullTranslations>`_
    and performs a similar function to `gettext.GNUTranslations
    <https://docs.python.org/2/library/gettext.html#
    the-gnutranslations-class>`_
    ; however, instead of using the translations in local ``mo`` files, it uses
    those provided by Globalization Pipeline (GP).

    NOTE: It is recommended that the ``GPTranslations`` constructor not be used
    directly - instead ``GPClient.translation`` or ``GPClient.gp_translation``
    should be used, which will create and return a ``GPTranslations`` instance.
    """
    __bundleId = None
    __languageId = None
    __client = None
    __cacheTimeout = None

    __cachedMap = {}
    __cacheMapTimestamp = None

    def __init__(self, client, bundleId, languageId, cacheTimeout, fp=None):
        NullTranslations.__init__(self, fp=fp)
        self.__client = client
        self.__bundleId = bundleId
        self.__languageId = languageId
        self.__cacheTimeout = cacheTimeout

    def gettext(self, message):
        """Contacts the GP service instance to find the translated value for
        the provided message key.

        If translated value is not available, and a fallback has been set,
        the fallback will be used. If there is no fallback, the source language
        value is returned. And if the message key is not found, the message
        key itself will be returned.

        The caching feature may be used to cache translated values locally
        in order to reduce the number of calls made to the GP service.

        * ``cacheTimeout = 0``, do not cache
        * ``cacheTimeout = -1``, cache forever
        * ``cacheTimeout > 0``, store cache value for specified number of \
            minutes

        """
        # cache forever or for specified time
        if self.__cacheTimeout == -1 or self.__cacheTimeout > 0:
            # get time passed since last cache
            if self.__cacheMapTimestamp:
                minutesPassed = (datetime.datetime.now() -
                    self.__cacheMapTimestamp).total_seconds() / 60

            # first call, or cache expired; initilize the cache
            if not self.__cacheMapTimestamp or (self.__cacheTimeout != -1 and
                minutesPassed >= self.__cacheTimeout):

                # set sourceFallback True if there is no Translations fallback
                sourceFallback = False if self._fallback else True

                self.__cachedMap = self.__client._GPClient__get_keys_map(
                    self.__bundleId, self.__languageId, fallback=sourceFallback)

                # only record the timestamp if caching is enabled
                if self.__cacheTimeout != 0:
                    self.__cacheMapTimestamp = datetime.datetime.now()

            # check cache for message key
            if self.__cachedMap:
                value = self.__cachedMap.get(message)
            else:
                value = None

            return self.__get_return_value(message, value)
        else:
            # no caching, get the translated value directly from GP service
            # set sourceFallback True if there is no Translations fallback
            sourceFallback = False if self._fallback else True
            tmpMap = self.__client._GPClient__get_keys_map(
                self.__bundleId, self.__languageId, fallback=sourceFallback)

            # check map for message key
            if tmpMap:
                value = tmpMap.get(message)
            else:
                value = None

            return self.__get_return_value(message, value)

    def __get_return_value(self, messageKey, value):
        """Determines the return value; used to prevent code duplication """
        # if value is not None, return it
        # otherwise, either use the Translations fallback if there is one,
        # or return the message key back
        if value:
            return value
        else:
            if self._fallback:
                return self._fallback.gettext(messageKey)
            else:
                return messageKey
