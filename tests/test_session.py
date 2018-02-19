# -*- coding: utf-8 -*-

from unittest import TestCase
from requests import Session
from flask import Flask
from flask_snow import Snow


class FlaskTestCase(TestCase):
    """Mix-in class for creating the Flask application."""

    def setUp(self):
        app = Flask(__name__)
        app.config['DEBUG'] = True
        app.config['TESTING'] = True

        app.config['SNOW_INSTANCE'] = 'mock_instance'

        app.logger.disabled = True
        self.app = app

    def tearDown(self):
        self.app = None


class TestSnow(FlaskTestCase):
    def test_session_object(self):
        """passing a session to init_app() should be of the same type as the object passed"""

        s = Session()

        snow = Snow()
        snow.init_app(self.app, session=s)

        with self.app.app_context():
            client = snow.connection['client']
            self.assertEqual(type(client.session), Session)



