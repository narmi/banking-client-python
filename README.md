# banking-client

- API version: 0.1.0
- Package version: 1.0.0
- Build package: io.swagger.codegen.languages.PythonClientCodegen

## Requirements.

Python 2.7 and 3.4+

## Installation & Usage
### pip install

If the python package is hosted on Github, you can install directly from Github

```sh
pip install git+https://github.com/narmitech/banking-client-python.git
```
(you may need to run `pip` with root permission: `sudo pip install git+https://github.com/narmitech/banking-client-python.git`)

Then import the package:
```python
import banking_client
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import banking_client
```

## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:

```python
from __future__ import print_function
import time
import banking_client
from banking_client.api_client import ApiClient
from banking_client.configuration import Configuration
from banking_client.rest import ApiException
from pprint import pprint

config = Configuration()
config.host = 'https://api.demo.narmitech.com/v1'
config.access_token = 'YOUR_ACCESS_TOKEN'
config.secret = 'YOUR_SECRET'
api_instance = banking_client.AccountApi(api_client=ApiClient(configuration=config))
api_instance.list()

try:
    # Get account
    api_response = api_instance.list()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AccountApi->get: %s\n" % e)

```

## Documentation for API Endpoints

All URIs are relative to *https://api.example.com/v1*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*AccountApi* | [**get**](docs/AccountApi.md#get) | **GET** /accounts/{accountId} | Get account
*AccountApi* | [**get_account_balances**](docs/AccountApi.md#get_account_balances) | **GET** /account_balances/{accountBalancesId} | Get account balances for an account
*AccountApi* | [**list**](docs/AccountApi.md#list) | **GET** /accounts | List accounts
*AccountApi* | [**list_account_balances**](docs/AccountApi.md#list_account_balances) | **GET** /account_balances | List account balances
*AccountApi* | [**update**](docs/AccountApi.md#update) | **PUT** /accounts/{accountId} | Update account
*GeneralApi* | [**list_ping**](docs/GeneralApi.md#list_ping) | **GET** /ping | Server heartbeat operation
*SubscriptionApi* | [**create**](docs/SubscriptionApi.md#create) | **POST** /subscriptions | Create subscription
*SubscriptionApi* | [**destroy**](docs/SubscriptionApi.md#destroy) | **DELETE** /subscriptions/{subscriptionId} | Delete subscription
*SubscriptionApi* | [**get**](docs/SubscriptionApi.md#get) | **GET** /subscriptions/{subscriptionId} | Get subscription
*SubscriptionApi* | [**list**](docs/SubscriptionApi.md#list) | **GET** /subscriptions | List subscriptions
*SubscriptionApi* | [**update**](docs/SubscriptionApi.md#update) | **PUT** /subscriptions/{subscriptionId} | Update subscription
*TransactionApi* | [**get**](docs/TransactionApi.md#get) | **GET** /transactions/{transactionId} | Get transaction
*TransactionApi* | [**list**](docs/TransactionApi.md#list) | **GET** /transactions | List transactions
*TransactionApi* | [**list_transactions**](docs/TransactionApi.md#list_transactions) | **GET** /accounts/{accountId}/transactions | List transactions for an account
*TransactionApi* | [**update**](docs/TransactionApi.md#update) | **PUT** /transactions/{transactionId} | Update transaction
*TransferApi* | [**create**](docs/TransferApi.md#create) | **POST** /transfers | Create a transfer
*UserApi* | [**get**](docs/UserApi.md#get) | **GET** /users/{userId} | Get user
*UserApi* | [**list**](docs/UserApi.md#list) | **GET** /users | List users


## Documentation For Models

 - [Account](docs/Account.md)
 - [AccountBalances](docs/AccountBalances.md)
 - [Address](docs/Address.md)
 - [Check](docs/Check.md)
 - [Document](docs/Document.md)
 - [Error](docs/Error.md)
 - [InlineResponse200](docs/InlineResponse200.md)
 - [InlineResponse2001](docs/InlineResponse2001.md)
 - [InlineResponse2002](docs/InlineResponse2002.md)
 - [InlineResponse2003](docs/InlineResponse2003.md)
 - [InlineResponse2004](docs/InlineResponse2004.md)
 - [InlineResponse2005](docs/InlineResponse2005.md)
 - [InlineResponse2006](docs/InlineResponse2006.md)
 - [InlineResponse2007](docs/InlineResponse2007.md)
 - [InlineResponse2008](docs/InlineResponse2008.md)
 - [InlineResponse201](docs/InlineResponse201.md)
 - [Links](docs/Links.md)
 - [Location](docs/Location.md)
 - [Membership](docs/Membership.md)
 - [Meta](docs/Meta.md)
 - [Phone](docs/Phone.md)
 - [Subscription](docs/Subscription.md)
 - [Transaction](docs/Transaction.md)
 - [Transfer](docs/Transfer.md)
 - [User](docs/User.md)


## Documentation For Authorization


## Application

- **Type**: OAuth
- **Flow**: application
- **Authorization URL**:
- **Scopes**:
 - **write**: allows reading and modifying resources
 - **read**: allows reading resources
 - **read:profile**: allows reading extended information about the user including address


## Author

contact@narmitech.com

