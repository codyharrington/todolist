Todolist
=============

This software is licensed under the MIT License. See LICENSE file for details.

This is my soon-to-be-deployed task tracking software. If you'd like to try it out for yourself, read on.

These installation instructions will probably be simplified at a later date. They have only been tested on a Linux system.

Requirements
---------------
* PostgreSQL
* git
* npm from Node.js
* Grunt
* Python 3 and pip
* virtualenv

Configuration
-----------------
To set up, simply modify config.py and change the Dbapi parameters.
Take a look inside rundbapi.py and runwebfront.py to adjust ports, etc

Installation
-------------
You'll want to enter your virtualenv here if you are going to use one
```sh
pip install -r requirements.txt
cd webfront/static
npm install
grunt
cd ..
```

Running the app(s):
--------------
Running is quite simple. The database is abstracted behind a REST API, so runs in a separate Flask app. This means that you have to have them both running for it to work. You'll also want to run them in separate terminals.

##### Database #####
```sh
python3 rundbapi.py
```
##### Web front end #####
```sh
python3 runwebfront.py
```

Contact
----------------
If you have any issues, log them on my github: https://github.com/codyharrington/todolist
