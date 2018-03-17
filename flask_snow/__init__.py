# -*- coding: utf-8 -*-

"""
    flask-snow
    ~~~~~~~~~~~~

    Adds pysnow (ServiceNow) support to Flask

    More information:
    https://github.com/rbw0/flask-snow
    https://github.com/rbw0/pysnow
"""

__author__ = "Robert Wikman <rbw@vault13.org>"
__version__ = "0.2.6"

import warnings

# noinspection PyProtectedMember
from flask import current_app, _app_ctx_stack as stack

from pysnow import Client, OAuthClient, ParamsBuilder

from .exceptions import ConfigError, InvalidUsage


class Snow(object):
    """Central controller class.
    Provides token_updater setter, context handling and basic / oauth client logic

    :param app: App to pass directly to Snow (if not using factory)
    """

    def __init__(self, app=None):
        self._client_type_oauth = self._client_type_basic = False
        self._session = None
        self._token_updater = None
        self._parameters = None

        if app is not None:
            self.init_app(app)

    def init_app(self, app, session=None, parameters=None):
        """Initializes snow extension

        Set config default and find out which client type to use

        :param app: App passed from constructor or directly to init_app (factory)
        :param session: requests-compatible session to pass along to init_app
        :param parameters: `ParamsBuilder` object passed to `Client` after instantiation
        :raises:
            - ConfigError - if unable to determine client type
        """

        if parameters is not None and not isinstance(parameters, ParamsBuilder):
            raise InvalidUsage("parameters should be a pysnow.ParamsBuilder object, not %r" % type(parameters).__name__)

        self._session = session
        self._parameters = parameters

        app.config.setdefault('SNOW_INSTANCE', None)
        app.config.setdefault('SNOW_HOST', None)
        app.config.setdefault('SNOW_USER', None)
        app.config.setdefault('SNOW_PASSWORD', None)
        app.config.setdefault('SNOW_OAUTH_CLIENT_ID', None)
        app.config.setdefault('SNOW_OAUTH_CLIENT_SECRET', None)
        app.config.setdefault('SNOW_USE_SSL', True)

        if app.config['SNOW_OAUTH_CLIENT_ID'] and app.config['SNOW_OAUTH_CLIENT_SECRET']:
            self._client_type_oauth = True
        elif self._session or (app.config['SNOW_USER'] and app.config['SNOW_PASSWORD']):
            self._client_type_basic = True
        else:
            raise ConfigError("You must supply user credentials, a session or OAuth credentials to use flask-snow")

    @property
    def token_updater(self):
        """Callback function called when a token update occurs

        Use to keep track of your user OAuth tokens::

            token_updater(updated_token):
                session['token'] = updated_token

            snow.init_app(app)
            snow.token_updater = token_updater
        """

        return self._token_updater

    @token_updater.setter
    def token_updater(self, token_updater):
        """Called when a token refresh occurs

        :token_updater: callback function receiving token updates
        :raises:
            - InvalidUsage - if not using oauth
        """

        if not self._client_type_oauth:
            raise InvalidUsage("Token updater can only be set if using OAuth")

        self._token_updater = token_updater

    def set_token(self, token):
        """Calls token_updater callback with the new token after updating the `pysnow.Client` object in the app context

        :param token: token dict returned from previous interactions with flask-snow
        """

        self.connection['client'].set_token(token)

        if self._token_updater:
            self._token_updater(token)

    def _get_basic_client(self):
        return Client(
            instance=current_app.config['SNOW_INSTANCE'],
            host=current_app.config['SNOW_HOST'],
            user=current_app.config['SNOW_USER'],
            password=current_app.config['SNOW_PASSWORD'],
            use_ssl=current_app.config['SNOW_USE_SSL'],
            session=self._session
        )

    def _get_oauth_client(self):
        return OAuthClient(
            instance=current_app.config['SNOW_INSTANCE'],
            host=current_app.config['SNOW_HOST'],
            client_id=current_app.config['SNOW_OAUTH_CLIENT_ID'],
            client_secret=current_app.config['SNOW_OAUTH_CLIENT_SECRET'],
            token_updater=self._token_updater,
            use_ssl=current_app.config['SNOW_USE_SSL']
        )

    def resource(self, *args, **kwargs):
        """Creates a new :class:`pysnow.Resource` object if it doesn't exist in its clients context

        :param args: args to pass along to pysnow.Resource
        :param kwargs: kwargs to pass along to pysnow.Resource
        :return: :class:`pysnow.Resource` object
        """

        resource_id = "pysnow__%s.%s" % (kwargs.get('base_path', '/api/now'), kwargs.get('api_path'))

        conn = self.connection

        if resource_id not in conn['resources']:
            # Create new resource and add to context
            conn['resources'].update({resource_id: conn['client'].resource(*args, **kwargs)})
        else:
            # Reuse object, reset sysparms
            conn['resources'][resource_id].parameters = conn['client'].parameters

        return conn['resources'][resource_id]

    @property
    def connection(self):
        """Snow connection instance, stores a `pysnow.Client` instance and `pysnow.Resource` instances

        Creates a new :class:`pysnow.Client` object if it doesn't exist in the app slice of the context stack

        :returns: :class:`pysnow.Client` object
        """

        ctx = stack.top.app
        if ctx is not None:
            if not hasattr(ctx, 'snow'):
                if self._client_type_oauth:
                    if not self._token_updater:
                        warnings.warn("No token updater has been set. Token refreshes will be ignored.")

                    client = self._get_oauth_client()
                else:
                    client = self._get_basic_client()

                if self._parameters:
                    # Set parameters passed on app init
                    client.parameters = self._parameters

                ctx.snow = {
                    'client': client,
                    'resources': {}
                }

            return ctx.snow
