# coding: utf-8

"""
    Narmi Banking API

    ## Introduction  This API is organized around REST. Our API has predictable, resource-oriented URLs, and uses HTTP response codes to indicate API errors.  ### Schema  JSON is returned by all API responses, including errors.  All timestamps return in ISO 8601 format: `YYYY-MM-DDTHH:MM:SSZ`.  ## Access  All API requests must be made over HTTPS. API requests without authentication will also fail.  Authentication to the API is via bearer authorization, for example using curl this would be `-H \"Authorization: Bearer $SECRET_KEY\"`.  Your API keys carry many privileges, so be sure to keep them secret! Do not share your secret API keys in publicly accessible areas such source code pushed to Github, client-side code, and so forth.  ### Request Signing  Requests to the production API must be signed, this requires use of the secret returned alongside the API token. This is done following [the draft specification on HTTP request signing](https://tools.ietf.org/html/draft-cavage-http-signatures-08).  This is a simple of example of signing only the `Date` header:  ``` token='1234acdefghijk' secret='acdefghijk1234' date=`date -u +'%Y-%m-%dT%H:%M:%SZ'` signature=`echo -n \"date: $date\" | openssl dgst -sha256 -binary -hmac \"$secret\" | base64` curl -H \"Authorization: Bearer $token\" -H \"Date: $date\" -H \"Signature: keyId=\\\"$token\\\",algorithm=\\\"hmac-sha256\\\",headers=\\\"date\\\",signature=\\\"$signature\\\"\" 'https://api.example.com/v1/accounts/' ```  For the production api, the following components of the signature are required:   * (request-target) psuedo header   * `Host` header   * `Date` header   * `Content-Type` header   * `Digest` header containing a digest of SHA-256 digest of the request body   * `Content-Length` header  A full signature header would look like:  ``` Signature: keyId=\"1234acdefghijk\",algorithm=\"hmac-sha256\",headers=\"(request-target),date,host,content-type,digest,content-length\",signature=\"zxywut321asdf\" ```  These signatures increase the security of production data in three ways: verifying the identity of the requester, protecting data in transit, and reducing the window of replay attacks.  Request signatures ensure that the request has been sent by someone with a valid access key and secret - even if the key was seen in transit, the secret should never be exposed and the signature depends on having a valid key and secret.  In addition, this prevents tampering with a request while it's in transit, since some of the request elements are used to calculate a digest of the request, and the resulting hash value is included as part of the request. If the value of the digest calculated by the API doesn't match, the digest in the request the API denies the request.  Finally, because a request must reach the API within five minutes of the timestamp in the request, a request is valid only for those five minutes.  ## Versions and resource stability  When we make backwards-incompatible changes to the API, we release new versions.  All requests will use your account API settings, unless you override the API version.  To set the API version on a specific request, send a `API-Version: '1234567'` header.  ### Stability  Within any given version of the API, any given resource (eg. /foos, /foo or /foos/:id/bars) has a specified level of stability. The stability of a resource is specified in the stability property.  The stability of a resource specifies what changes will be made to the resource and how changes will be communicated. The possible types of changes are detailed below. All changes are communicated in the api changelog.  There are three levels of stability: prototype, development, and production.  #### Prototype  A prototype resource is experimental and major changes are likely. In time, a prototype resource may or may not advance to production.  * Compatible and emergency changes may be made with no advance notice * Disruptive changes may be made with one week notice * Deprecated resources will remain available for at least one month after deprecation  #### Development  A Development resource is a work-in-progress, but major changes should be infrequent. Development resources should advance to production stability in time.  * Compatible and emergency changes may be made with no advance notice * Disruptive changes may be made with one month notice * Deprecated resources will remain available for at least six months after deprecation  #### Production  A production resources is complete and major changes will no longer occur.  * Compatible and emergency changes may be made with no advance notice * Disruptive changes may not occur, instead a new major version is developed * Deprecated resources will remain available for at least twelve months after deprecation  ### Deprecation  Deprecated resources have a deprecated_at date property which is also displayed in the documentation. Deprecated resources will keep working for at least as long after deprecation as mandated by their stability: 1 month for prototype resources, 6 month for development resources and 12 months for production resources. Deprecated resources will not change stability.  Once a resource has been completely deactivated, it will return HTTP 410 for all requests.  ### Types of changes  #### Compatible change  Small in scope and unlikely to break or change semantics of existing methods.  * Add resources, methods and attributes * Change documentation * Change undocumented behavior  #### Disruptive change  May have larger impact and effort will be made to provide migration paths as needed.  * Change semantics of existing methods * Remove resources, methods and attributes  #### Emergency change  May have larger impact, but are unavoidable due to legal compliance, security vulnerabilities or violation of specification.  ## Requests and responses  ### Requests  An endpoint's name indicates the type of data it handles and the action it performs on that data. The most common actions are:  | Action |  HTTP Method | Description | | ------ | ------------ | ----------- | | Create  |  POST |  Creates and persists an entity of the corresponding type. | | List  |  GET |   Returns all instances of a particular entity that match query parameters you provide. | | Retrieve  |  GET |   Returns the single instance of an entity that matches the identifier you provide. | | Update  |  PUT |   Modifies the existing entity that matches the identifier you provide. | | Delete  |  DELETE |  Deletes the existing entity that matches the identifier you provide. Deleted entities cannot be retrieved or undeleted. |  All requests must include a header indicating the format of the resposne to be returned:  ``` Accept: application/json ```  #### Providing parameters  The way you provide parameters to a request depends on the HTTP method of the request.  ##### `GET` and `DELETE`  For GET and DELETE requests, you provide parameters in a query string you append to your request's URL. For example,  ``` /v1/locations/$LOCATION_ID/transactions?sort_order=ASC ```  Values for query parameters must be URL-escaped.  ##### `POST`, `PUT` and `PATCH`  For `POST`, `PUT` and `PATCH` requests, you instead provide parameters as JSON in the body of your request. POST and PUT requests must include one additional header:  ``` Content-Type: application/json ```  And in the body of the request:  ``` {   \"given_name\": \"Amelia\",   \"family_name\": \"Earhart\" } ```  ### Responses  [Conventional HTTP response codes](https://httpstatuses.com/) indicate the success or failure of an API request, not all errors map cleanly onto HTTP response codes, however. In general:  | HTTP Response code | Indication | | ------------------ | ---------- | | 2xx                | success    | | 4xx                | an error that failed given the information provided (e.g., a required parameter was omitted, or the configuration does is invalid, etc.) | | 5xx                | 5xx range indicate an error processing the request |  #### Response bodies  When a request is successful, a response body will typically be sent back in the form of a JSON object and include a `Content-Type: application/json` header. One exception to this is when a DELETE request is processed, which will result in a successful HTTP 204 status and an empty response body.  Inside of this JSON object, the resource root that was the target of the request will be set as the key. This will be the singular form of the word if the request operated on a single object, and the plural form of the word if a collection was processed.  #### Response meta-information  Responses will have a [top level `meta` key](http://jsonapi.org/format/#document-meta) with meta information associated with the request. Common keys include:  | key | description | example | | --- | ----------- | ------- | | deprecated_at | | | | stability | | | | total | used in paginating responses | |  #### Errors  Failing responses will have an appropriate status and a JSON body containing more details about a particular error.  | Name | Type | Description |  Example | | ---- | ---- | ----------- | ---------- | | id |  string |  id of error raised | \"rate_limit\" | | message |   string |  end user message of error raised | \"Your account reached the API limit. Please wait a few minutes before making new requests\" | | url |   string |  reference url with more information about the error  | https://example.com/developer/articles/rate-limits |  ## Pagination  Requests that return multiple items will be paginated to 25 items by default. You can specify subsequent pages with the `page` query parameter. For some resources, you can also set a custom page size up to `100` with the `per_page` parameter. A top level object in the response body named `links` will contain full URLs to access the next and previous pages of the response.  ``` { ... \"links\": {   \"next\": \"https://api.example.com/v1/accounts?page=2\",   \"previous\": \"https://api.example.com/v1/accounts?page=1\" } ... } ```  For endpoints that return resources that have an inherent temporal order (for example transactions, for which one transaction must follow another), cursors are supported. The `before` and `after` query parameters allow cursor like pagination, where the value of each is the id of the resource to continue pagination.  ## Filtering  List (index) endpoints sometimes expose query parameters which allow the responses to be limited to resources matching the given filters.  In the case that an invalid filter value is specified a status code of 404 with a detailed explanation is returned.  ## Working with money  We support different currencies, for resources in all of these currencies, the amount is in the smallest common currency unit - this is the amount in cents (or pence, or similarly named unit). For example, to specify for $1.00 or 1.00, you would set amount=100 (100 cents of the respective currency).  For zero-decimal currencies, we use the regular denomination. For example, a transaction of 1 Yen, you should set amount=1 (1 JPY), since 1 is the smallest currency unit.  ## Request IDs  Each API request has an associated request identifier in the response headers, under Request-Id. You can also find request identifiers in the URLs of individual request logs in your Dashboard. If you need to contact us about a specific request, providing the request identifier will ensure the fastest possible resolution.   # noqa: E501

    OpenAPI spec version: 0.1.0
    Contact: contact@narmitech.com
"""


from __future__ import absolute_import

import copy
import logging
import multiprocessing
import sys
import urllib3

import six
from six.moves import http_client as httplib


class TypeWithDefault(type):
    def __init__(cls, name, bases, dct):
        super(TypeWithDefault, cls).__init__(name, bases, dct)
        cls._default = None

    def __call__(cls):
        if cls._default is None:
            cls._default = type.__call__(cls)
        return copy.copy(cls._default)

    def set_default(cls, default):
        cls._default = copy.copy(default)


class Configuration(six.with_metaclass(TypeWithDefault, object)):
    """
    This class is auto generated, do not edit the class manually.
    """

    def __init__(self):
        """Constructor"""
        # Default Base url
        self.host = "https://api.example.com/v1"
        # Temp file folder for downloading files
        self.temp_folder_path = None

        # Authentication Settings
        # dict to store API key(s)
        self.api_key = {}
        # dict to store API prefix (e.g. Bearer)
        self.api_key_prefix = {}
        # Username for HTTP basic authentication
        self.username = ""
        # Password for HTTP basic authentication
        self.password = ""

        # access token for OAuth
        self.access_token = ""
        self.secret = ""

        # Logging Settings
        self.logger = {}
        self.logger["package_logger"] = logging.getLogger("banking_client")
        self.logger["urllib3_logger"] = logging.getLogger("urllib3")
        # Log format
        self.logger_format = '%(asctime)s %(levelname)s %(message)s'
        # Log stream handler
        self.logger_stream_handler = None
        # Log file handler
        self.logger_file_handler = None
        # Debug file location
        self.logger_file = None
        # Debug switch
        self.debug = False

        # SSL/TLS verification
        # Set this to false to skip verifying SSL certificate when calling API
        # from https server.
        self.verify_ssl = True
        # Set this to customize the certificate file to verify the peer.
        self.ssl_ca_cert = None
        # client certificate file
        self.cert_file = None
        # client key file
        self.key_file = None
        # Set this to True/False to enable/disable SSL hostname verification.
        self.assert_hostname = None

        # urllib3 connection pool's maximum number of connections saved
        # per pool. urllib3 uses 1 connection as default value, but this is
        # not the best value when you are making a lot of possibly parallel
        # requests to the same host, which is often the case here.
        # cpu_count * 5 is used as default value to increase performance.
        self.connection_pool_maxsize = multiprocessing.cpu_count() * 5

        # Proxy URL
        self.proxy = None
        # Safe chars for path_param
        self.safe_chars_for_path_param = ''

    @property
    def logger_file(self):
        """The logger file.

        If the logger_file is None, then add stream handler and remove file
        handler. Otherwise, add file handler and remove stream handler.

        :param value: The logger_file path.
        :type: str
        """
        return self.__logger_file

    @logger_file.setter
    def logger_file(self, value):
        """The logger file.

        If the logger_file is None, then add stream handler and remove file
        handler. Otherwise, add file handler and remove stream handler.

        :param value: The logger_file path.
        :type: str
        """
        self.__logger_file = value
        if self.__logger_file:
            # If set logging file,
            # then add file handler and remove stream handler.
            self.logger_file_handler = logging.FileHandler(self.__logger_file)
            self.logger_file_handler.setFormatter(self.logger_formatter)
            for _, logger in six.iteritems(self.logger):
                logger.addHandler(self.logger_file_handler)
                if self.logger_stream_handler:
                    logger.removeHandler(self.logger_stream_handler)
        else:
            # If not set logging file,
            # then add stream handler and remove file handler.
            self.logger_stream_handler = logging.StreamHandler()
            self.logger_stream_handler.setFormatter(self.logger_formatter)
            for _, logger in six.iteritems(self.logger):
                logger.addHandler(self.logger_stream_handler)
                if self.logger_file_handler:
                    logger.removeHandler(self.logger_file_handler)

    @property
    def debug(self):
        """Debug status

        :param value: The debug status, True or False.
        :type: bool
        """
        return self.__debug

    @debug.setter
    def debug(self, value):
        """Debug status

        :param value: The debug status, True or False.
        :type: bool
        """
        self.__debug = value
        if self.__debug:
            # if debug status is True, turn on debug logging
            for _, logger in six.iteritems(self.logger):
                logger.setLevel(logging.DEBUG)
            # turn on httplib debug
            httplib.HTTPConnection.debuglevel = 1
        else:
            # if debug status is False, turn off debug logging,
            # setting log level to default `logging.WARNING`
            for _, logger in six.iteritems(self.logger):
                logger.setLevel(logging.WARNING)
            # turn off httplib debug
            httplib.HTTPConnection.debuglevel = 0

    @property
    def logger_format(self):
        """The logger format.

        The logger_formatter will be updated when sets logger_format.

        :param value: The format string.
        :type: str
        """
        return self.__logger_format

    @logger_format.setter
    def logger_format(self, value):
        """The logger format.

        The logger_formatter will be updated when sets logger_format.

        :param value: The format string.
        :type: str
        """
        self.__logger_format = value
        self.logger_formatter = logging.Formatter(self.__logger_format)

    def get_api_key_with_prefix(self, identifier):
        """Gets API key (with prefix if set).

        :param identifier: The identifier of apiKey.
        :return: The token for api key authentication.
        """
        if (self.api_key.get(identifier) and
                self.api_key_prefix.get(identifier)):
            return self.api_key_prefix[identifier] + ' ' + self.api_key[identifier]  # noqa: E501
        elif self.api_key.get(identifier):
            return self.api_key[identifier]

    def get_basic_auth_token(self):
        """Gets HTTP basic authentication header (string).

        :return: The token for basic HTTP authentication.
        """
        return urllib3.util.make_headers(
            basic_auth=self.username + ':' + self.password
        ).get('authorization')

    def auth_settings(self):
        """Gets Auth Settings dict for api client.

        :return: The Auth Settings information dict.
        """
        return {

            'Application':
                {
                    'type': 'oauth2',
                    'in': 'header',
                    'key': 'Authorization',
                    'value': 'Bearer ' + self.access_token,
                    'token': self.access_token,
                    'secret': self.secret
                },

        }

    def to_debug_report(self):
        """Gets the essential information for debugging.

        :return: The report for debugging.
        """
        return "Python SDK Debug Report:\n"\
               "OS: {env}\n"\
               "Python Version: {pyversion}\n"\
               "Version of the API: 0.1.0\n"\
               "SDK Package Version: 1.0.0".\
               format(env=sys.platform, pyversion=sys.version)
