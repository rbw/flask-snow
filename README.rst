.. image:: https://coveralls.io/repos/github/rbw0/flask-snow/badge.svg?branch=master
    :target: https://coveralls.io/github/rbw0/flask-snow?branch=master
.. image:: https://travis-ci.org/rbw0/flask-snow.svg?branch=master
    :target: https://travis-ci.org/rbw0/flask-snow
.. image:: https://badge.fury.io/py/flask-snow.svg
    :target: https://pypi.python.org/pypi/flask-snow
.. image:: https://img.shields.io/badge/License-MIT-green.svg
    :target: https://opensource.org/licenses/MIT
    
flask-snow
============

Easily create apps on top of the ServiceNow REST API.

- Uses the lightweight `Flask microframework <http://flask.pocoo.org>`_ and the `pysnow library <https://github.com/rbw0/pysnow>`_.
- Supports OAuth for a seamless authentication / authorization experience.


Documentation
-------------
The documentation can be found `here <http://flask-snow.readthedocs.org/>`_


Installation
------------

    $ pip install flask-snow

Usage
-----

Minimal example.

Reads *config*, sets up the *snow extension* and creates a route at **/incidents**, returning a single incident by number.

.. code-block:: python

    from flask import Flask, request, jsonify
    from flask_snow import Snow

    app = Flask(__name__)
    app.config.from_object('settings')

    snow = Snow(app)

    @app.route('/incidents/<number>')
    def incident(number):
        incident = snow.resource(api_path='/table/incident')
        data = incident.get(query={'number': number}).one()
        return jsonify(data)

    if __name__ == '__main__':
        app.run()


Name it **server.py** and run with ``python server.py``


Check out the /examples for more!


Compatibility
-------------
- Python 2 and 3
- Flask > 0.9

Author
------
Created by Robert Wikman <rbw@vault13.org> in 2018

JetBrains
---------
Thank you `Jetbrains <www.jetbrains.com>`_ for creating pycharm and for providing me with free licenses


