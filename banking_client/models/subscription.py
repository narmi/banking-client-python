# coding: utf-8

"""
    Narmi Banking API

    ## Introduction  This API is organized around REST. Our API has predictable, resource-oriented URLs, and uses HTTP response codes to indicate API errors.  ### Schema  JSON is returned by all API responses, including errors.  All timestamps return in ISO 8601 format: `YYYY-MM-DDTHH:MM:SSZ`.  ## Access  All API requests must be made over HTTPS. API requests without authentication will also fail.  Authentication to the API is via bearer authorization, for example using curl this would be `-H \"Authorization: Bearer $SECRET_KEY\"`.  Your API keys carry many privileges, so be sure to keep them secret! Do not share your secret API keys in publicly accessible areas such source code pushed to Github, client-side code, and so forth.  ### Request Signing  Requests to the production API must be signed, this requires use of the secret returned alongside the API token. This is done following [the draft specification on HTTP request signing](https://tools.ietf.org/html/draft-cavage-http-signatures-08).  This is a simple of example of signing only the `Date` header:  ``` token='1234acdefghijk' secret='acdefghijk1234' date=`date -u +'%Y-%m-%dT%H:%M:%SZ'` signature=`echo -n \"date: $date\" | openssl dgst -sha256 -binary -hmac \"$secret\" | base64` curl -H \"Authorization: Bearer $token\" -H \"Date: $date\" -H \"Signature: keyId=\\\"$token\\\",algorithm=\\\"hmac-sha256\\\",headers=\\\"date\\\",signature=\\\"$signature\\\"\" 'https://api.example.com/v1/accounts/' ```  For the production api, the following components of the signature are required:   * (request-target) psuedo header   * `Host` header   * `Date` header   * `Content-Type` header   * `Digest` header containing a digest of SHA-256 digest of the request body   * `Content-Length` header  A full signature header would look like:  ``` Signature: keyId=\"1234acdefghijk\",algorithm=\"hmac-sha256\",headers=\"(request-target),date,host,content-type,digest,content-length\",signature=\"zxywut321asdf\" ```  These signatures increase the security of production data in three ways: verifying the identity of the requester, protecting data in transit, and reducing the window of replay attacks.  Request signatures ensure that the request has been sent by someone with a valid access key and secret - even if the key was seen in transit, the secret should never be exposed and the signature depends on having a valid key and secret.  In addition, this prevents tampering with a request while it's in transit, since some of the request elements are used to calculate a digest of the request, and the resulting hash value is included as part of the request. If the value of the digest calculated by the API doesn't match, the digest in the request the API denies the request.  Finally, because a request must reach the API within five minutes of the timestamp in the request, a request is valid only for those five minutes.  ## Versions and resource stability  When we make backwards-incompatible changes to the API, we release new versions.  All requests will use your account API settings, unless you override the API version.  To set the API version on a specific request, send a `API-Version: '1234567'` header.  ### Stability  Within any given version of the API, any given resource (eg. /foos, /foo or /foos/:id/bars) has a specified level of stability. The stability of a resource is specified in the stability property.  The stability of a resource specifies what changes will be made to the resource and how changes will be communicated. The possible types of changes are detailed below. All changes are communicated in the api changelog.  There are three levels of stability: prototype, development, and production.  #### Prototype  A prototype resource is experimental and major changes are likely. In time, a prototype resource may or may not advance to production.  * Compatible and emergency changes may be made with no advance notice * Disruptive changes may be made with one week notice * Deprecated resources will remain available for at least one month after deprecation  #### Development  A Development resource is a work-in-progress, but major changes should be infrequent. Development resources should advance to production stability in time.  * Compatible and emergency changes may be made with no advance notice * Disruptive changes may be made with one month notice * Deprecated resources will remain available for at least six months after deprecation  #### Production  A production resources is complete and major changes will no longer occur.  * Compatible and emergency changes may be made with no advance notice * Disruptive changes may not occur, instead a new major version is developed * Deprecated resources will remain available for at least twelve months after deprecation  ### Deprecation  Deprecated resources have a deprecated_at date property which is also displayed in the documentation. Deprecated resources will keep working for at least as long after deprecation as mandated by their stability: 1 month for prototype resources, 6 month for development resources and 12 months for production resources. Deprecated resources will not change stability.  Once a resource has been completely deactivated, it will return HTTP 410 for all requests.  ### Types of changes  #### Compatible change  Small in scope and unlikely to break or change semantics of existing methods.  * Add resources, methods and attributes * Change documentation * Change undocumented behavior  #### Disruptive change  May have larger impact and effort will be made to provide migration paths as needed.  * Change semantics of existing methods * Remove resources, methods and attributes  #### Emergency change  May have larger impact, but are unavoidable due to legal compliance, security vulnerabilities or violation of specification.  ## Requests and responses  ### Requests  An endpoint's name indicates the type of data it handles and the action it performs on that data. The most common actions are:  | Action |  HTTP Method | Description | | ------ | ------------ | ----------- | | Create  |  POST |  Creates and persists an entity of the corresponding type. | | List  |  GET |   Returns all instances of a particular entity that match query parameters you provide. | | Retrieve  |  GET |   Returns the single instance of an entity that matches the identifier you provide. | | Update  |  PUT |   Modifies the existing entity that matches the identifier you provide. | | Delete  |  DELETE |  Deletes the existing entity that matches the identifier you provide. Deleted entities cannot be retrieved or undeleted. |  All requests must include a header indicating the format of the resposne to be returned:  ``` Accept: application/json ```  #### Providing parameters  The way you provide parameters to a request depends on the HTTP method of the request.  ##### `GET` and `DELETE`  For GET and DELETE requests, you provide parameters in a query string you append to your request's URL. For example,  ``` /v1/locations/$LOCATION_ID/transactions?sort_order=ASC ```  Values for query parameters must be URL-escaped.  ##### `POST`, `PUT` and `PATCH`  For `POST`, `PUT` and `PATCH` requests, you instead provide parameters as JSON in the body of your request. POST and PUT requests must include one additional header:  ``` Content-Type: application/json ```  And in the body of the request:  ``` {   \"given_name\": \"Amelia\",   \"family_name\": \"Earhart\" } ```  ### Responses  [Conventional HTTP response codes](https://httpstatuses.com/) indicate the success or failure of an API request, not all errors map cleanly onto HTTP response codes, however. In general:  | HTTP Response code | Indication | | ------------------ | ---------- | | 2xx                | success    | | 4xx                | an error that failed given the information provided (e.g., a required parameter was omitted, or the configuration does is invalid, etc.) | | 5xx                | 5xx range indicate an error processing the request |  #### Response bodies  When a request is successful, a response body will typically be sent back in the form of a JSON object and include a `Content-Type: application/json` header. One exception to this is when a DELETE request is processed, which will result in a successful HTTP 204 status and an empty response body.  Inside of this JSON object, the resource root that was the target of the request will be set as the key. This will be the singular form of the word if the request operated on a single object, and the plural form of the word if a collection was processed.  #### Response meta-information  Responses will have a [top level `meta` key](http://jsonapi.org/format/#document-meta) with meta information associated with the request. Common keys include:  | key | description | example | | --- | ----------- | ------- | | deprecated_at | | | | stability | | | | total | used in paginating responses | |  #### Errors  Failing responses will have an appropriate status and a JSON body containing more details about a particular error.  | Name | Type | Description |  Example | | ---- | ---- | ----------- | ---------- | | id |  string |  id of error raised | \"rate_limit\" | | message |   string |  end user message of error raised | \"Your account reached the API limit. Please wait a few minutes before making new requests\" | | url |   string |  reference url with more information about the error  | https://example.com/developer/articles/rate-limits |  ## Pagination  Requests that return multiple items will be paginated to 25 items by default. You can specify subsequent pages with the `page` query parameter. For some resources, you can also set a custom page size up to `100` with the `per_page` parameter. A top level object in the response body named `links` will contain full URLs to access the next and previous pages of the response.  ``` { ... \"links\": {   \"next\": \"https://api.example.com/v1/accounts?page=2\",   \"previous\": \"https://api.example.com/v1/accounts?page=1\" } ... } ```  For endpoints that return resources that have an inherent temporal order (for example transactions, for which one transaction must follow another), cursors are supported. The `before` and `after` query parameters allow cursor like pagination, where the value of each is the id of the resource to continue pagination.  ## Filtering  List (index) endpoints sometimes expose query parameters which allow the responses to be limited to resources matching the given filters.  In the case that an invalid filter value is specified a status code of 404 with a detailed explanation is returned.  ## Working with money  We support different currencies, for resources in all of these currencies, the amount is in the smallest common currency unit - this is the amount in cents (or pence, or similarly named unit). For example, to specify for $1.00 or 1.00, you would set amount=100 (100 cents of the respective currency).  For zero-decimal currencies, we use the regular denomination. For example, a transaction of 1 Yen, you should set amount=1 (1 JPY), since 1 is the smallest currency unit.  ## Request IDs  Each API request has an associated request identifier in the response headers, under Request-Id. You can also find request identifiers in the URLs of individual request logs in your Dashboard. If you need to contact us about a specific request, providing the request identifier will ensure the fastest possible resolution.   # noqa: E501

    OpenAPI spec version: 0.1.0
    Contact: contact@narmitech.com
"""


import pprint
import re  # noqa: F401

import six


class Subscription(object):
    """
    This class is auto generated, do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'id': 'str',
        'subscription': 'str',
        'description': 'str',
        'url': 'str',
        'secret': 'str',
        'version': 'str',
        'is_active': 'bool',
        'created_at': 'datetime',
        'updated_at': 'datetime'
    }

    attribute_map = {
        'id': 'id',
        'subscription': 'subscription',
        'description': 'description',
        'url': 'url',
        'secret': 'secret',
        'version': 'version',
        'is_active': 'is_active',
        'created_at': 'created_at',
        'updated_at': 'updated_at'
    }

    def __init__(self, id=None, subscription=None, description=None, url=None, secret=None, version=None, is_active=None, created_at=None, updated_at=None):  # noqa: E501
        """Subscription - a model defined in Swagger"""  # noqa: E501

        self._id = None
        self._subscription = None
        self._description = None
        self._url = None
        self._secret = None
        self._version = None
        self._is_active = None
        self._created_at = None
        self._updated_at = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if subscription is not None:
            self.subscription = subscription
        if description is not None:
            self.description = description
        if url is not None:
            self.url = url
        if secret is not None:
            self.secret = secret
        if version is not None:
            self.version = version
        if is_active is not None:
            self.is_active = is_active
        if created_at is not None:
            self.created_at = created_at
        if updated_at is not None:
            self.updated_at = updated_at

    @property
    def id(self):
        """Gets the id of this Subscription.  # noqa: E501

        Subscription ID, opaque unique identifier  # noqa: E501

        :return: The id of this Subscription.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Subscription.

        Subscription ID, opaque unique identifier  # noqa: E501

        :param id: The id of this Subscription.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def subscription(self):
        """Gets the subscription of this Subscription.  # noqa: E501

        name of event to respond to, ie resource.create, resource.*  # noqa: E501

        :return: The subscription of this Subscription.  # noqa: E501
        :rtype: str
        """
        return self._subscription

    @subscription.setter
    def subscription(self, subscription):
        """Sets the subscription of this Subscription.

        name of event to respond to, ie resource.create, resource.*  # noqa: E501

        :param subscription: The subscription of this Subscription.  # noqa: E501
        :type: str
        """

        self._subscription = subscription

    @property
    def description(self):
        """Gets the description of this Subscription.  # noqa: E501

        human readable description of hook (e.g. my special foo)  # noqa: E501

        :return: The description of this Subscription.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this Subscription.

        human readable description of hook (e.g. my special foo)  # noqa: E501

        :param description: The description of this Subscription.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def url(self):
        """Gets the url of this Subscription.  # noqa: E501

        URL to which events will POST  # noqa: E501

        :return: The url of this Subscription.  # noqa: E501
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """Sets the url of this Subscription.

        URL to which events will POST  # noqa: E501

        :param url: The url of this Subscription.  # noqa: E501
        :type: str
        """

        self._url = url

    @property
    def secret(self):
        """Gets the secret of this Subscription.  # noqa: E501


        :return: The secret of this Subscription.  # noqa: E501
        :rtype: str
        """
        return self._secret

    @secret.setter
    def secret(self, secret):
        """Sets the secret of this Subscription.


        :param secret: The secret of this Subscription.  # noqa: E501
        :type: str
        """

        self._secret = secret

    @property
    def version(self):
        """Gets the version of this Subscription.  # noqa: E501


        :return: The version of this Subscription.  # noqa: E501
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this Subscription.


        :param version: The version of this Subscription.  # noqa: E501
        :type: str
        """

        self._version = version

    @property
    def is_active(self):
        """Gets the is_active of this Subscription.  # noqa: E501


        :return: The is_active of this Subscription.  # noqa: E501
        :rtype: bool
        """
        return self._is_active

    @is_active.setter
    def is_active(self, is_active):
        """Sets the is_active of this Subscription.


        :param is_active: The is_active of this Subscription.  # noqa: E501
        :type: bool
        """

        self._is_active = is_active

    @property
    def created_at(self):
        """Gets the created_at of this Subscription.  # noqa: E501


        :return: The created_at of this Subscription.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this Subscription.


        :param created_at: The created_at of this Subscription.  # noqa: E501
        :type: datetime
        """

        self._created_at = created_at

    @property
    def updated_at(self):
        """Gets the updated_at of this Subscription.  # noqa: E501


        :return: The updated_at of this Subscription.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this Subscription.


        :param updated_at: The updated_at of this Subscription.  # noqa: E501
        :type: datetime
        """

        self._updated_at = updated_at

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Subscription):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
