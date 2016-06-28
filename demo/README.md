<!-- Copyright IBM Corp. 2015

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License. -->

What is this?
-------------
This is a demo Python app which uses the Globalization Pipeline service on
Bluemix. Note that this app is designed to be run on Bluemix.

A running instance of the demo can be found [here](
http://gp-python-client-demo.mybluemix.net/).

Prepare demo
-------------
In order to run the demo, you must first create a new Globalization Pipeline
service instance. You can name the instance whatever you'd like, but the
manifest.yml` file must be updated to reflect the name, currently the
service instance name is `Globalization Pipeline-py-demo.

Next, create a new bundle in this instance and name it `demo`; you can use
another name, but `main.py` must then be updated accordingly.

Use `messages.json` as the source file and select as many target languages
as you'd like.

Run the demo
------------
Once the necessary files have been updated. You can push the app to Bluemix.

You can either use the cf cli or push to Bluemix using git. You can search
around on Bluemix for the necessary documentation.

If you use the cf cli, simply go to the demo dir and run `cf push`.
