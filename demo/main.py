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

import os, logging
from gpclient import GPClient, GPServiceAccount, GPTranslations
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
@app.route('/index.html')
def root():
    # 1 - create GPServiceAccount
    # if the app is running on Bluemix, the credentials will be obtained
    # from the VCAP environment variable
    acc = None
    try:
        acc = GPServiceAccount()
    except AssertionError:
        logging.error('Unable to create GPServiceAccount')
        return

    # 2 - create Globalization Pipeline client
    # the client is responsible for communication with the service
    client = GPClient(acc)

    bundleId='demo'

    # for the demo, get all avalible languages in the bundle
    # normally, this should equal to the language of the locale
    languages = client.get_avaliable_languages(bundleId=bundleId)

    messages = []

    for language in languages:
        # 3 - create translation instance
        # Note: because we are displaying the translations for all avalible
        # languages, a new translation instance is create each time;
        # normally, only one instance for the language of choice is required
        t = client.translation(bundleId=bundleId, languages=[language])

        # 4 - create a shortcut for the function
        _ = t.gettext

        # 5 - get the translated value from Globalization Pipeline service
        # by calling the shortcut
        translatedValue = _('welcome')

        messages.append({'language': language, 'welcome': translatedValue})

    return render_template('index.html', messages=messages)

# Run app
# VCAP_APP_PORT should be set by bluemix
port = os.getenv('PORT', '5000')
if __name__ == '__main__':
    # listen to all public IPs on specified port
    app.run(host='0.0.0.0', port=int(port))
