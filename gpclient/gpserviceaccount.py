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
import re


class GPServiceAccount():
    """Holds authentication details for connecting to the Globalization
       Pipeline (GP) service instance. The service supports Globalization
       Pipeline Authentication and Identity and Access Management (IAM) authentication

    There are three options for creating a ``GPServiceAccount`` instance:

        1. Provide the parameters.
        Mandatory for both authentication mechanisms
        ``url``, ``instanceId``
        For Globalization Pipeline authentication:
        ``userId`` and ``password``
        For IAM authentication:
        ``apiKey``

        If both Globalization Pipeline and IAM authentication credentials are provided then ``GPServiceAccount``
        instance will be initialized with Globalization Pipeline authentication.


        2. Use the user defined environment variables (no params required).
        Mandatory for both authentication mechanisms:
        ``GPServiceAccount.GP_URL_ENV_VAR``,
        ``GPServiceAccount.GP_INSTANCE_ID_ENV_VAR``

        For Globalization Pipeline authentication:
        ``GPServiceAccount.GP_USER_ID_ENV_VAR``,
        ``GPServiceAccount.GP_PASSWORD_ENV_VAR``

        For IAM authentication:
        ``GPServiceAccount.GP_IAM_API_KEY_ENV_VAR``

        If both Globalization Pipeline and IAM authentication credentials are provided then ``GPServiceAccount``
        instance will be initialized with Globalization Pipeline authentication.

        3. Search the ``VCAP_SERVICES`` environment variable for all avaliable
        GP service instances. If a service instance name is provided, it will
        be given precedence. (optional ``serviceInstanceName`` param)
    """

    # check these user defined env vars if they are set
    GP_URL_ENV_VAR              = "GP_URL"
    GP_INSTANCE_ID_ENV_VAR      = "GP_INSTANCE_ID"
    GP_USER_ID_ENV_VAR          = "GP_USER_ID"
    GP_PASSWORD_ENV_VAR         = "GP_PASSWORD"
    GP_IAM_API_KEY_ENV_VAR      = "GP_IAM_API_KEY"

    # check VCAP_SERVICES env var and extract data if necessary
    # (see app's VCAP_SERVICES env var for json template)
    __VCAP_SERVICES_ENV_VAR     = "VCAP_SERVICES"
    __NAME_KEY                  = 'name'
    __CREDENTIALS_KEY           = 'credentials'
    __INSTANCE_ID_KEY           = 'instanceId'
    __URL_KEY                   = 'url'
    __USER_ID_KEY               = 'userId'
    __PASSWORD_KEY              = 'password'
    __IAM_API_KEY_KEY           = 'apikey'

    __gpServiceNameRegex = re.compile('^g11n-pipeline|^gp-')

    __url = None
    __instanceId = None
    __userId = None
    __password = None
    __apiKey = None
    __iamEnabled = None

    def __setcreds__(self, url, instanceId, userId, password):
        self.__url = url
        self.__instanceId = instanceId
        self.__userId = userId
        self.__password = password
        self.__iamEnabled = False

    def __setIamCreds__(self, url, instanceId, apiKey):
        self.__url = url
        self.__instanceId = instanceId
        self.__apiKey = apiKey
        self.__iamEnabled = True


    def __init__(self, url=None, instanceId=None, userId=None, password=None,
                 serviceInstanceName=None, credentialsJson=None, apiKey=None):
        credentialsSet = False
        if url and instanceId:
            logging.info('Trying to initialize by params')
            if userId and password:
                self.__setcreds__(url, instanceId, userId, password)
                credentialsSet = True
                logging.info('using user provided data to create GPServiceAccount supporting GP auth.')
            elif apiKey:
                self.__setIamCreds__(url, instanceId, apiKey)
                credentialsSet = True
                logging.info('using user provided data to create GPServiceAccount supporting IAM auth.')
            if credentialsSet:
                logging.info('Successfully completed initialization by params')
        if not credentialsSet:
            logging.info('Trying to initialize by user env')
            (url, instanceId, userId, password, apiKey) = self.__get_user_env_vars()
            if url and instanceId:
                if userId and password:
                    self.__setcreds__(url, instanceId, userId, password)
                    credentialsSet = True
                    logging.info("""using user defined environment variables to
                        create GPServiceAccount""")
                elif apiKey:
                    self.__setIamCreds__(url, instanceId, apiKey)
                    credentialsSet = True
                    logging.info("""using user defined environment variables to
                                    create GPServiceAccount supporting IAM auth.""")
            if credentialsSet:
                logging.info('Successfully completed initialization by user env variables')
        if not credentialsSet and credentialsJson is not None:
            logging.info('Trying to initialize by credentials file')
            (url, instanceId, userId, password, apiKey) = self.__get_credentials_from_file(credentialsJson)
            if url and instanceId:
                if userId and password:
                    self.__setcreds__(url, instanceId, userId, password)
                    credentialsSet = True
                    logging.info("""using user defined environment variables to
                        create GPServiceAccount""")
                elif apiKey:
                    self.__setcreds__(url, instanceId, apiKey)
                    credentialsSet = True
                    logging.info("""using user defined environment variables to
                        create GPServiceAccount supporting IAM auth.""")
            if credentialsSet:
                logging.info('Successfully completed initialization by credentials file')
        if not credentialsSet:
            logging.info('Trying to initialize by vcap_services env var')
            (url, instanceId, userId, password, apiKey) = \
                    self.__parse_vcap_services_env_var(serviceInstanceName)
            if url and instanceId:
                if userId and password:
                    self.__setcreds__(url, instanceId, userId, password)
                    credentialsSet = True
                    logging.info("""using VCAP_SERVICES environment variable to
                            create GPServiceAccount""")
                elif apiKey:
                    self.__setIamCreds__(url, instanceId, apiKey)
                    credentialsSet = True
                    logging.info("""using VCAP_SERVICES environment variable to
                            create GPServiceAccount supporting IAM auth.""")
            if credentialsSet:
                logging.info('Successfully completed initialization by vcap_services env var')
        # make sure that all the vars are set
        if not credentialsSet:
            logging.error("Failed to initialize service account by any of the available init methods.")
        assert self.__url, ('url is not a string: <%s>' % self.__url)
        assert self.__instanceId, ('instanceId is not a string: <%s>' %self.__instanceId)
        if self.__iamEnabled:
            assert self.__apiKey, ('apiKey is not a string: <%s>' %self.__apiKey)
            logging.info(('created GPServiceAccount supporting IAM auth using url <%s>, ' + \
                          'instanceId <%s>, and IAM API Key <***>'), self.__url,
                         self.__instanceId, self.__userId)
        else:
            assert self.__userId, ('userId is not a string: <%s>' %self.__userId)
            assert self.__password, ('password is not a string: <%s>' %self.__password)
            logging.info(('created GPServiceAccount using url <%s>, ' + \
            'instanceId <%s>, userId <%s>, and password <***>'), self.__url,
            self.__instanceId, self.__userId)

    def get_url(self):
        """Return the ``url`` being used by this ``GPServiceAccount``"""
        return self.__url

    def get_instance_id(self):
        """Return the ``instanceId`` being used by this ``GPServiceAccount``"""
        return self.__instanceId

    def get_user_id(self):
        """Return the ``userId`` being used by this ``GPServiceAccount``"""
        return self.__userId

    def get_password(self):
        """Return the ``password`` being used by this ``GPServiceAccount``"""
        return self.__password

    def get_api_key(self):
        """Return the ``IAM API Key`` being used by this ``GPServiceAccount``"""
        return self.__apiKey

    def is_iam_enabled(self):
        """Return true if the ``GPServiceAccount`` being used is IAM enabled"""
        return self.__iamEnabled
    
    def __get_credentials_from_file(self, credsFile):
        credsJson = open(credsFile, "r")
        credentials = json.load(credsJson)
        if credentials and "credentials" in credentials:
            # credentials: { ... }
            credentials = credentials["credentials"]
        if credentials:
            return (credentials["url"], credentials["instanceId"], credentials["userId"], credentials["password"], credentials["apikey"])
        return (None, None, None, None, None)
            

    def __get_user_env_vars(self):
        """Return the user defined environment variables"""
        return (os.environ.get(self.GP_URL_ENV_VAR),
            os.environ.get(self.GP_INSTANCE_ID_ENV_VAR),
            os.environ.get(self.GP_USER_ID_ENV_VAR),
            os.environ.get(self.GP_PASSWORD_ENV_VAR),
            os.environ.get(self.GP_IAM_API_KEY_ENV_VAR))

    def __parse_vcap_services_env_var(self, serviceInstanceName=None):
        """Parse the ``VCAP_SERVICES`` env var and search for the necessary
        values
        """
        vcapServices = os.environ.get(self.__VCAP_SERVICES_ENV_VAR)

        if not vcapServices:
            return (None, None, None, None, None)

        parsedVcapServices = json.loads(vcapServices)

        gpServicesInstances = []
        for serviceName in parsedVcapServices:
            if self.__gpServiceNameRegex.match(serviceName):
                serviceInstances = parsedVcapServices.get(serviceName)
                for serviceInstance in serviceInstances:
                    gpServicesInstances.append(serviceInstance)

        if not gpServicesInstances:
            return (None, None, None, None, None)

        targetGPServiceInstance = None
        # use first service if no name is provided
        if not serviceInstanceName:
            targetGPServiceInstance = gpServicesInstances[0]
        else:
            # search for service name
            for gpServiceInstance in gpServicesInstances:
                if gpServiceInstance.get(self.__NAME_KEY)== serviceInstanceName:
                    targetGPServiceInstance = gpServiceInstance
                    break

        # service was not found
        if not targetGPServiceInstance:
            return  (None, None, None, None, None)

        credentials = targetGPServiceInstance.get(self.__CREDENTIALS_KEY)

        if not credentials:
            return (None, None, None, None, None)

        url = credentials.get(self.__URL_KEY)
        instanceId = credentials.get(self.__INSTANCE_ID_KEY)
        userId = credentials.get(self.__USER_ID_KEY)
        password = credentials.get(self.__PASSWORD_KEY)
        apiKey = credentials.get(self.__IAM_API_KEY_KEY)

        return (url, instanceId, userId, password, apiKey)
