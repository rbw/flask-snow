flask-snow
=============

.. module:: flask_snow

Adds ServiceNow support to Flask.


Installation
------------

Use pip to install the extension::

    $ pip install flask-snow


Usage
-----

flask-snow is managed through a ``Snow`` instance::

    from flask import Flask
    from flask_snow import Snow

    app = Flask(__name__)
    snow = Snow(app)

you may also set up your ``Snow`` instance later using **init_app** method::

    snow = Snow()

    app = Flask(__name__)
    snow.init_app(app)


Once created, resources may be created::

    incident = snow.resource(api_path='/table/incident')
    record = incident.get(query={}, limit=1).first()


Check out the `pysnow API documentation <http://pysnow.readthedocs.io/en/latest>`_ for more info.


Configuration
-------------

The following configuration values exist for flask-snow.

========================== ============== ================
Name                       Default value  Description
========================== ============== ================
SNOW_INSTANCE              None           Instance name
SNOW_HOST                  None           FQDN (instead of instance)
SNOW_USE_SSL               True           Whether or not to use SSL
SNOW_RAISE_ON_EMPTY        False          Raise an exception on empty result sets
========================== ============== ================

Authentication
^^^^^^^^^^^^^^
The following authentication methods are supported:

- Static - Set a static username and password to use for all requests
- Oauth - set client id and secret, and authenticate users in the application context
- session - pre-made requests-compatible session

**Static**

========================== ============== ================
Name                       Default value  Description
========================== ============== ================
SNOW_USER                  None           Username
SNOW_PASSWORD              None           Password
========================== ============== ================


**Oauth**

========================== ============== ================
Name                       Default value  Description
========================== ============== ================
SNOW_OAUTH_CLIENT_ID       None           Client ID (from ServiceNow)
SNOW_OAUTH_CLIENT_SECRET   None           Client secret (from ServiceNow)
========================== ============== ================

**Session**

Passing a custom **session** to `flask-snow` doesn't require any configuration. Simply::

    import requests
    from flask import Flask
    from flask_snow import Snow

    s = requests.Session()

    # Lets disable SSL verification
    s.verify = False
    s.auth = requests.auth.HTTPBasicAuth('myusername', 'mypassword')

    snow = Snow()

    app = Flask(__name__)
    snow.init_app(app, session=s)


Examples
--------

Full examples can be found `here <https://github.com/rbw0/flask-snow/tree/master/examples>`_



API
---

.. autoclass:: flask_snow.Snow
    :members:

