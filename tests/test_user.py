# -*- coding: utf-8 -*-

from unittest import TestCase
from flask import Flask
from pysnow import Client
from flask_snow import Snow
from flask_snow.exceptions import ConfigError, InvalidUsage


class FlaskTestCase(TestCase):
    """Mix-in class for creating the Flask application."""

    def setUp(self):
        app = Flask(__name__)
        app.config['DEBUG'] = True
        app.config['TESTING'] = True

        app.config['SNOW_INSTANCE'] = 'mock_instance'
        app.config['SNOW_USER'] = 'mock_user'
        app.config['SNOW_PASSWORD'] = 'mock_password'

        app.logger.disabled = True
        self.app = app

    def tearDown(self):
        self.app = None


class TestSnow(FlaskTestCase):
    def test_constructor(self):
        Snow(self.app)

    def test_init_app(self):
        snow = Snow()
        if hasattr(self.app, 'extensions'):
            del self.app.extensions

        snow.init_app(self.app)

    def test_missing_config(self):
        """flask_snow.Snow should raise ConfigError if a required OAuth setting is missing"""

        snow = Snow()
        test1 = test2 = self.app

        test1.config.pop('SNOW_USER')
        self.assertRaises(ConfigError, snow.init_app, test1)

        test2.config.pop('SNOW_PASSWORD')
        self.assertRaises(ConfigError, snow.init_app, test2)

    def test_client_type(self):
        """setting SNOW_USER and SNOW_PASSWORD should set type Snow._client_type_basic to True"""

        snow = Snow()
        snow.init_app(self.app)

        # oauth should be True
        self.assertEqual(snow._client_type_oauth, False)

        # basic should be False
        self.assertEqual(snow._client_type_basic, True)

    def test_token_updater(self):
        """Setting token_updater for non-oauth client should raise an InvalidUsage error"""
        def token_updater():
            pass

        def token_setter():
            snow.token_updater = token_updater

        snow = Snow()
        snow.init_app(self.app)

        self.assertRaises(InvalidUsage, token_setter)

    def test_user_connect(self):
        """client set in connection context should be an instance of pysnow.Client"""

        snow = Snow()
        snow.init_app(self.app)

        with self.app.app_context():
            client = snow.connection['client']
            self.assertEqual(type(client), Client)
