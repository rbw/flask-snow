# -*- coding: utf-8 -*-

from functools import wraps

from logging.config import dictConfig

from flask import Flask, session, abort, jsonify, request
from pysnow.exceptions import TokenCreateError

from requests.exceptions import HTTPError
from flask_snow import Snow

app = Flask(__name__)
app.config.from_object('settings')

# Configure logging, specifically for the pysnow library
dictConfig(app.config['LOGGING'])

snow = Snow()
snow.init_app(app)


def token_updater(updated_token):
    app.logger.info('refreshing token!')
    session['token'] = updated_token


snow.token_updater = token_updater


def snow_resource(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if not session.get('token'):
            abort(401, {'error': 'you must be authenticated to access this resource'})

        if not snow.token:
            snow.set_token(session['token'])

        try:
            return f(*args, **kwargs)
        except HTTPError as e:
            abort(e.response.status_code)

    return inner


@app.route('/auth')
def auth():
    qs = request.args
    username = qs.get('username')
    password = qs.get('password')

    if not (username and password):
        abort(401, {'error': 'you must provide a username and password'})

    try:
        session['token'] = snow.connection.generate_token(username, password)
        return jsonify({'result': 'authentication successful!'})
    except TokenCreateError as e:
        if e.snow_status_code == 400 and e.description == 'access_denied':
            code = 401
        else:
            code = e.snow_status_code

        abort(code, e.__dict__)


@app.route('/incidents')
@snow_resource
def incident_list():
    limit = request.args.get('limit') or 10
    
    r = snow.connection.resource(api_path='/table/incident')
    data = r.get(query={}, limit=limit).all()

    return jsonify(list(data))


@app.route('/incidents/<number>')
@snow_resource
def incident(number):
    r = snow.connection.resource(api_path='/table/incident')
    data = r.get(query={'number': number}).one()

    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
