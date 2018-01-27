# coding: utf-8

"""
    Narmi Banking API

    ## Introduction  This API is organized around REST. Our API has predictable, resource-oriented URLs, and uses HTTP response codes to indicate API errors.  ### Schema  JSON is returned by all API responses, including errors.  All timestamps return in ISO 8601 format: `YYYY-MM-DDTHH:MM:SSZ`.  ## Access  All API requests must be made over HTTPS. API requests without authentication will also fail.  Authentication to the API is via bearer authorization, for example using curl this would be `-H \"Authorization: Bearer $SECRET_KEY\"`.  Your API keys carry many privileges, so be sure to keep them secret! Do not share your secret API keys in publicly accessible areas such source code pushed to Github, client-side code, and so forth.  ### Request Signing  Requests to the production API must be signed, this requires use of the secret returned alongside the API token. This is done following [the draft specification on HTTP request signing](https://tools.ietf.org/html/draft-cavage-http-signatures-08).  This is a simple of example of signing only the `Date` header:  ``` token='1234acdefghijk' secret='acdefghijk1234' date=`date -u +'%Y-%m-%dT%H:%M:%SZ'` signature=`echo -n \"date: $date\" | openssl dgst -sha256 -binary -hmac \"$secret\" | base64` curl -H \"Authorization: Bearer $token\" -H \"Date: $date\" -H \"Signature: keyId=\\\"$token\\\",algorithm=\\\"hmac-sha256\\\",headers=\\\"date\\\",signature=\\\"$signature\\\"\" 'https://api.example.com/v1/accounts/' ```  For the production api, the following components of the signature are required:   * (request-target) psuedo header   * `Host` header   * `Date` header   * `Content-Type` header   * `Digest` header containing a digest of SHA-256 digest of the request body   * `Content-Length` header  A full signature header would look like:  ``` Signature: keyId=\"1234acdefghijk\",algorithm=\"hmac-sha256\",headers=\"(request-target),date,host,content-type,digest,content-length\",signature=\"zxywut321asdf\" ```  These signatures increase the security of production data in three ways: verifying the identity of the requester, protecting data in transit, and reducing the window of replay attacks.  Request signatures ensure that the request has been sent by someone with a valid access key and secret - even if the key was seen in transit, the secret should never be exposed and the signature depends on having a valid key and secret.  In addition, this prevents tampering with a request while it's in transit, since some of the request elements are used to calculate a digest of the request, and the resulting hash value is included as part of the request. If the value of the digest calculated by the API doesn't match, the digest in the request the API denies the request.  Finally, because a request must reach the API within five minutes of the timestamp in the request, a request is valid only for those five minutes.  ## Versions and resource stability  When we make backwards-incompatible changes to the API, we release new versions.  All requests will use your account API settings, unless you override the API version.  To set the API version on a specific request, send a `API-Version: '1234567'` header.  ### Stability  Within any given version of the API, any given resource (eg. /foos, /foo or /foos/:id/bars) has a specified level of stability. The stability of a resource is specified in the stability property.  The stability of a resource specifies what changes will be made to the resource and how changes will be communicated. The possible types of changes are detailed below. All changes are communicated in the api changelog.  There are three levels of stability: prototype, development, and production.  #### Prototype  A prototype resource is experimental and major changes are likely. In time, a prototype resource may or may not advance to production.  * Compatible and emergency changes may be made with no advance notice * Disruptive changes may be made with one week notice * Deprecated resources will remain available for at least one month after deprecation  #### Development  A Development resource is a work-in-progress, but major changes should be infrequent. Development resources should advance to production stability in time.  * Compatible and emergency changes may be made with no advance notice * Disruptive changes may be made with one month notice * Deprecated resources will remain available for at least six months after deprecation  #### Production  A production resources is complete and major changes will no longer occur.  * Compatible and emergency changes may be made with no advance notice * Disruptive changes may not occur, instead a new major version is developed * Deprecated resources will remain available for at least twelve months after deprecation  ### Deprecation  Deprecated resources have a deprecated_at date property which is also displayed in the documentation. Deprecated resources will keep working for at least as long after deprecation as mandated by their stability: 1 month for prototype resources, 6 month for development resources and 12 months for production resources. Deprecated resources will not change stability.  Once a resource has been completely deactivated, it will return HTTP 410 for all requests.  ### Types of changes  #### Compatible change  Small in scope and unlikely to break or change semantics of existing methods.  * Add resources, methods and attributes * Change documentation * Change undocumented behavior  #### Disruptive change  May have larger impact and effort will be made to provide migration paths as needed.  * Change semantics of existing methods * Remove resources, methods and attributes  #### Emergency change  May have larger impact, but are unavoidable due to legal compliance, security vulnerabilities or violation of specification.  ## Requests and responses  ### Requests  An endpoint's name indicates the type of data it handles and the action it performs on that data. The most common actions are:  | Action |  HTTP Method | Description | | ------ | ------------ | ----------- | | Create  |  POST |  Creates and persists an entity of the corresponding type. | | List  |  GET |   Returns all instances of a particular entity that match query parameters you provide. | | Retrieve  |  GET |   Returns the single instance of an entity that matches the identifier you provide. | | Update  |  PUT |   Modifies the existing entity that matches the identifier you provide. | | Delete  |  DELETE |  Deletes the existing entity that matches the identifier you provide. Deleted entities cannot be retrieved or undeleted. |  All requests must include a header indicating the format of the resposne to be returned:  ``` Accept: application/json ```  #### Providing parameters  The way you provide parameters to a request depends on the HTTP method of the request.  ##### `GET` and `DELETE`  For GET and DELETE requests, you provide parameters in a query string you append to your request's URL. For example,  ``` /v1/locations/$LOCATION_ID/transactions?sort_order=ASC ```  Values for query parameters must be URL-escaped.  ##### `POST`, `PUT` and `PATCH`  For `POST`, `PUT` and `PATCH` requests, you instead provide parameters as JSON in the body of your request. POST and PUT requests must include one additional header:  ``` Content-Type: application/json ```  And in the body of the request:  ``` {   \"given_name\": \"Amelia\",   \"family_name\": \"Earhart\" } ```  ### Responses  [Conventional HTTP response codes](https://httpstatuses.com/) indicate the success or failure of an API request, not all errors map cleanly onto HTTP response codes, however. In general:  | HTTP Response code | Indication | | ------------------ | ---------- | | 2xx                | success    | | 4xx                | an error that failed given the information provided (e.g., a required parameter was omitted, or the configuration does is invalid, etc.) | | 5xx                | 5xx range indicate an error processing the request |  #### Response bodies  When a request is successful, a response body will typically be sent back in the form of a JSON object and include a `Content-Type: application/json` header. One exception to this is when a DELETE request is processed, which will result in a successful HTTP 204 status and an empty response body.  Inside of this JSON object, the resource root that was the target of the request will be set as the key. This will be the singular form of the word if the request operated on a single object, and the plural form of the word if a collection was processed.  #### Response meta-information  Responses will have a [top level `meta` key](http://jsonapi.org/format/#document-meta) with meta information associated with the request. Common keys include:  | key | description | example | | --- | ----------- | ------- | | deprecated_at | | | | stability | | | | total | used in paginating responses | |  #### Errors  Failing responses will have an appropriate status and a JSON body containing more details about a particular error.  | Name | Type | Description |  Example | | ---- | ---- | ----------- | ---------- | | id |  string |  id of error raised | \"rate_limit\" | | message |   string |  end user message of error raised | \"Your account reached the API limit. Please wait a few minutes before making new requests\" | | url |   string |  reference url with more information about the error  | https://example.com/developer/articles/rate-limits |  ## Pagination  Requests that return multiple items will be paginated to 25 items by default. You can specify subsequent pages with the `page` query parameter. For some resources, you can also set a custom page size up to `100` with the `per_page` parameter. A top level object in the response body named `links` will contain full URLs to access the next and previous pages of the response.  ``` { ... \"links\": {   \"next\": \"https://api.example.com/v1/accounts?page=2\",   \"previous\": \"https://api.example.com/v1/accounts?page=1\" } ... } ```  For endpoints that return resources that have an inherent temporal order (for example transactions, for which one transaction must follow another), cursors are supported. The `before` and `after` query parameters allow cursor like pagination, where the value of each is the id of the resource to continue pagination.  ## Filtering  List (index) endpoints sometimes expose query parameters which allow the responses to be limited to resources matching the given filters.  In the case that an invalid filter value is specified a status code of 404 with a detailed explanation is returned.  ## Working with money  We support different currencies, for resources in all of these currencies, the amount is in the smallest common currency unit - this is the amount in cents (or pence, or similarly named unit). For example, to specify for $1.00 or 1.00, you would set amount=100 (100 cents of the respective currency).  For zero-decimal currencies, we use the regular denomination. For example, a transaction of 1 Yen, you should set amount=1 (1 JPY), since 1 is the smallest currency unit.  ## Request IDs  Each API request has an associated request identifier in the response headers, under Request-Id. You can also find request identifiers in the URLs of individual request logs in your Dashboard. If you need to contact us about a specific request, providing the request identifier will ensure the fastest possible resolution.   # noqa: E501

    OpenAPI spec version: 0.1.0
    Contact: contact@narmitech.com
"""


from __future__ import absolute_import

import io
import json
import logging
import re
import ssl

import certifi
# python 2 and python 3 compatibility library
import six
from six.moves.urllib.parse import urlencode

try:
    import urllib3
except ImportError:
    raise ImportError('python client requires urllib3.')


logger = logging.getLogger(__name__)


class RESTResponse(io.IOBase):

    def __init__(self, resp):
        self.urllib3_response = resp
        self.status = resp.status
        self.reason = resp.reason
        self.data = resp.data

    def getheaders(self):
        """Returns a dictionary of the response headers."""
        return self.urllib3_response.getheaders()

    def getheader(self, name, default=None):
        """Returns a given response header."""
        return self.urllib3_response.getheader(name, default)


class RESTClientObject(object):

    def __init__(self, configuration, pools_size=4, maxsize=None):
        # urllib3.PoolManager will pass all kw parameters to connectionpool
        # https://github.com/shazow/urllib3/blob/f9409436f83aeb79fbaf090181cd81b784f1b8ce/urllib3/poolmanager.py#L75  # noqa: E501
        # https://github.com/shazow/urllib3/blob/f9409436f83aeb79fbaf090181cd81b784f1b8ce/urllib3/connectionpool.py#L680  # noqa: E501
        # maxsize is the number of requests to host that are allowed in parallel  # noqa: E501
        # Custom SSL certificates and client certificates: http://urllib3.readthedocs.io/en/latest/advanced-usage.html  # noqa: E501

        # cert_reqs
        if configuration.verify_ssl:
            cert_reqs = ssl.CERT_REQUIRED
        else:
            cert_reqs = ssl.CERT_NONE

        # ca_certs
        if configuration.ssl_ca_cert:
            ca_certs = configuration.ssl_ca_cert
        else:
            # if not set certificate file, use Mozilla's root certificates.
            ca_certs = certifi.where()

        addition_pool_args = {}
        if configuration.assert_hostname is not None:
            addition_pool_args['assert_hostname'] = configuration.assert_hostname  # noqa: E501

        if maxsize is None:
            if configuration.connection_pool_maxsize is not None:
                maxsize = configuration.connection_pool_maxsize
            else:
                maxsize = 4

        # https pool manager
        if configuration.proxy:
            self.pool_manager = urllib3.ProxyManager(
                num_pools=pools_size,
                maxsize=maxsize,
                cert_reqs=cert_reqs,
                ca_certs=ca_certs,
                cert_file=configuration.cert_file,
                key_file=configuration.key_file,
                proxy_url=configuration.proxy,
                **addition_pool_args
            )
        else:
            self.pool_manager = urllib3.PoolManager(
                num_pools=pools_size,
                maxsize=maxsize,
                cert_reqs=cert_reqs,
                ca_certs=ca_certs,
                cert_file=configuration.cert_file,
                key_file=configuration.key_file,
                **addition_pool_args
            )

    def request(self, method, url, query_params=None, headers=None,
                body=None, post_params=None, _preload_content=True,
                _request_timeout=None):
        """Perform requests.

        :param method: http request method
        :param url: http request url
        :param query_params: query parameters in the url
        :param headers: http request headers
        :param body: request json body, for `application/json`
        :param post_params: request post parameters,
                            `application/x-www-form-urlencoded`
                            and `multipart/form-data`
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        """
        method = method.upper()
        assert method in ['GET', 'HEAD', 'DELETE', 'POST', 'PUT',
                          'PATCH', 'OPTIONS']

        if post_params and body:
            raise ValueError(
                "body parameter cannot be used with post_params parameter."
            )

        post_params = post_params or {}
        headers = headers or {}

        timeout = None
        if _request_timeout:
            if isinstance(_request_timeout, (int, ) if six.PY3 else (int, long)):  # noqa: E501,F821
                timeout = urllib3.Timeout(total=_request_timeout)
            elif (isinstance(_request_timeout, tuple) and
                  len(_request_timeout) == 2):
                timeout = urllib3.Timeout(
                    connect=_request_timeout[0], read=_request_timeout[1])

        if 'Content-Type' not in headers:
            headers['Content-Type'] = 'application/json'

        try:
            # For `POST`, `PUT`, `PATCH`, `OPTIONS`, `DELETE`
            if method in ['POST', 'PUT', 'PATCH', 'OPTIONS', 'DELETE']:
                if query_params:
                    url += '?' + urlencode(query_params)
                if re.search('json', headers['Content-Type'], re.IGNORECASE):
                    request_body = None
                    if body is not None:
                        request_body = json.dumps(body)
                    r = self.pool_manager.request(
                        method, url,
                        body=request_body,
                        preload_content=_preload_content,
                        timeout=timeout,
                        headers=headers)
                elif headers['Content-Type'] == 'application/x-www-form-urlencoded':  # noqa: E501
                    r = self.pool_manager.request(
                        method, url,
                        fields=post_params,
                        encode_multipart=False,
                        preload_content=_preload_content,
                        timeout=timeout,
                        headers=headers)
                elif headers['Content-Type'] == 'multipart/form-data':
                    # must del headers['Content-Type'], or the correct
                    # Content-Type which generated by urllib3 will be
                    # overwritten.
                    del headers['Content-Type']
                    r = self.pool_manager.request(
                        method, url,
                        fields=post_params,
                        encode_multipart=True,
                        preload_content=_preload_content,
                        timeout=timeout,
                        headers=headers)
                # Pass a `string` parameter directly in the body to support
                # other content types than Json when `body` argument is
                # provided in serialized form
                elif isinstance(body, str):
                    request_body = body
                    r = self.pool_manager.request(
                        method, url,
                        body=request_body,
                        preload_content=_preload_content,
                        timeout=timeout,
                        headers=headers)
                else:
                    # Cannot generate the request from given parameters
                    msg = """Cannot prepare a request message for provided
                             arguments. Please check that your arguments match
                             declared content type."""
                    raise ApiException(status=0, reason=msg)
            # For `GET`, `HEAD`
            else:
                r = self.pool_manager.request(method, url,
                                              fields=query_params,
                                              preload_content=_preload_content,
                                              timeout=timeout,
                                              headers=headers)
        except urllib3.exceptions.SSLError as e:
            msg = "{0}\n{1}".format(type(e).__name__, str(e))
            raise ApiException(status=0, reason=msg)

        if _preload_content:
            r = RESTResponse(r)

            # In the python 3, the response.data is bytes.
            # we need to decode it to string.
            if six.PY3:
                r.data = r.data.decode('utf8')

            # log response body
            logger.debug("response body: %s", r.data)

        if not 200 <= r.status <= 299:
            raise ApiException(http_resp=r)

        return r

    def GET(self, url, headers=None, query_params=None, _preload_content=True,
            _request_timeout=None):
        return self.request("GET", url,
                            headers=headers,
                            _preload_content=_preload_content,
                            _request_timeout=_request_timeout,
                            query_params=query_params)

    def HEAD(self, url, headers=None, query_params=None, _preload_content=True,
             _request_timeout=None):
        return self.request("HEAD", url,
                            headers=headers,
                            _preload_content=_preload_content,
                            _request_timeout=_request_timeout,
                            query_params=query_params)

    def OPTIONS(self, url, headers=None, query_params=None, post_params=None,
                body=None, _preload_content=True, _request_timeout=None):
        return self.request("OPTIONS", url,
                            headers=headers,
                            query_params=query_params,
                            post_params=post_params,
                            _preload_content=_preload_content,
                            _request_timeout=_request_timeout,
                            body=body)

    def DELETE(self, url, headers=None, query_params=None, body=None,
               _preload_content=True, _request_timeout=None):
        return self.request("DELETE", url,
                            headers=headers,
                            query_params=query_params,
                            _preload_content=_preload_content,
                            _request_timeout=_request_timeout,
                            body=body)

    def POST(self, url, headers=None, query_params=None, post_params=None,
             body=None, _preload_content=True, _request_timeout=None):
        return self.request("POST", url,
                            headers=headers,
                            query_params=query_params,
                            post_params=post_params,
                            _preload_content=_preload_content,
                            _request_timeout=_request_timeout,
                            body=body)

    def PUT(self, url, headers=None, query_params=None, post_params=None,
            body=None, _preload_content=True, _request_timeout=None):
        return self.request("PUT", url,
                            headers=headers,
                            query_params=query_params,
                            post_params=post_params,
                            _preload_content=_preload_content,
                            _request_timeout=_request_timeout,
                            body=body)

    def PATCH(self, url, headers=None, query_params=None, post_params=None,
              body=None, _preload_content=True, _request_timeout=None):
        return self.request("PATCH", url,
                            headers=headers,
                            query_params=query_params,
                            post_params=post_params,
                            _preload_content=_preload_content,
                            _request_timeout=_request_timeout,
                            body=body)


class ApiException(Exception):

    def __init__(self, status=None, reason=None, http_resp=None):
        if http_resp:
            self.status = http_resp.status
            self.reason = http_resp.reason
            self.body = http_resp.data
            self.headers = http_resp.getheaders()
        else:
            self.status = status
            self.reason = reason
            self.body = None
            self.headers = None

    def __str__(self):
        """Custom error messages for exception"""
        error_message = "({0})\n"\
                        "Reason: {1}\n".format(self.status, self.reason)
        if self.headers:
            error_message += "HTTP response headers: {0}\n".format(
                self.headers)

        if self.body:
            error_message += "HTTP response body: {0}\n".format(self.body)

        return error_message
