API relay with OAuth
--------------------

This example shows how Flask can be used with flask-snow to create a simple API server that uses OAuth and relays requests/responses.

The **/incidents** resource(s) uses the ``snow_resource`` decorator, which

- Ensures the client has a token and prints the appropriate error message if not
- Checks for and handles HTTP response errors thrown by the pysnow library


Usage
-----
1) Install requirements::

  $ pip install -r requirements.txt

2) Set ``SNOW_INSTANCE``, ``SNOW_OAUTH_CLIENT_ID``, ``SNOW_OAUTH_CLIENT_SECRET``

3) Start the server::

  $ python server.py

4) Open your browser and authenticate:: 
  
  `http://127.0.0.1:5000/auth?username=<username>&password=<password>`


You should now be able to obtain a list of incidents::

  http://127.0.0.1:5000/incidents


Or get a single incident by number::

  http://127.0.0.1:5000/incidents/INC012345


You just got your own little ServiceNow API server relay with seamless authentication and authorization. Happy days.

