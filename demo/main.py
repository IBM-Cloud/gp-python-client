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

import os, locale, logging, json, gettext
from gpclient import GPClient, GPServiceAccount, GPTranslations
from flask  import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/index.html')
def demo():
    ## 1 - create GPServiceAccount
    acc = None
    try:
        acc = GPServiceAccount()
    except AssertionError:
        logging.error('Unable to create GPServiceAccount')
        return

    ## 2 - create Globalization Pipeline client
    client = GPClient(acc)

    # bundle containing the source strings
    bundleId='demo'

    languages = client.get_avaliable_languages(bundleId=bundleId)

    messages = []

    for language in languages:
        ## 3 - create translation instance
        # Note: because we are displaying the translations for all avalible
        # languages, a new translation instance is create each time;
        # normally, only one instance for the language of choice is required
        t = client.translation(bundleId=bundleId, languages=[language])
        _ = t.gettext

        # get the translated value from Globalization Pipeline service
        welcomeValue =  _('welcome')

        messages.append({'language': language,
                        'welcome': welcomeValue})

    return render_template('index.html', messages=messages)

# VCAP_APP_PORT should be set by bluemix
port = os.getenv('VCAP_APP_PORT', '5000')
if __name__ == '__main__':
    # listen to all public IPs on specified port
	app.run(host='0.0.0.0', port=int(port))
