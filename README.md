Todolist
=============
This software is licensed under the MIT License. See LICENSE file for details.

This is task tracking software. If you'd like to try it out for yourself, read on.

These installation instructions will probably be simplified at a later date. They have only been tested on a Linux system.

![Build Status](https://jenkins.harringtonca.com/job/todolist/badge/icon)](https://jenkins.harringtonca.com/job/todolist/)

Requirements
---------------
You'll need to make sure all of the following packages are installed on your system before you continue:
* postgresql
* git
* nodejs
* npm (usually comes with nodejs)
* python3
* python3-pip
* python-virtualenv
* python-dev
* build-essential (This may be optional; distros like Arch Linux do not require it)

Configuration
-----------------
To set up, simply modify config.py and change the Dbapi parameters. You can also use a local_config.py
which has the same layout as config.py. Any values in this local_config will overwrite the same ones in config.py,
and local_config.py is in the gitignore, so you can put sensitive configuration values there that you don't want
committed.

Take a look inside rundbapi.py and runwebfront.py to adjust ports, etc

Installation
-------------
Once everything is configured, installing the dependencies is straightforward. Assuming you're in the terminal,
at the base directory of the project, follow the steps below.

Create a virtualenv called venv that uses Python 3:
```sh
virtualenv -p $(which python3) venv
```
Activate the virtualenv:
```sh
source venv/bin/activate
```
Install python dependencies (with python 3 pip)
```sh
pip3 install -r requirements.txt
```
Install javascript dependencies
```sh
cd webfront/static
npm install
grunt
```
...and we're done (assuming there were no errors).

Running the app(s):
------------------
Running is quite simple. The database is abstracted behind a REST API, so runs in a separate Flask app. This means that you have to have them both running for it to work. You'll also want to run them in separate terminals.

Note that you'll need to activate the virtualenv for both of these applications

##### Database #####
```sh
python3 rundbapi.py
```
##### Web front end #####
```sh
python3 runwebfront.py
```

Deploying the app:
-----------------
For deployment, I use gunicorn and Nginx. Here's a brief description of how I've gone about it:

webfront is running from gunicorn locally on 127.0.0.1, on a port that isn't 80. I use Nginx as a reverse proxy
to forward web traffic to it. You can find plenty of guides for setting up Flask + gunicorn + Nginx floating around
the internet.

dbapi is running from gunicorn on 127.0.0.1 as well. This doesn't need to be exposed to the web until I've made the
ReST API public, as webfront makes all the connections to it locally.

When I want to deploy new changes, I simply push them to my repo, then run a script which automatically pulls from
git on the server end, then restarts the apps.

About the database ReST API
---------------------------
The database has been abstracted away into a separate application, and all queries and commits
are performed via JSON to and from different URIs. It follows that serialisation and de-serialisation happens at
each end.

The reason for doing this is so I can potentially implement a different database backend, possibly even
in a different language. An API spec will be written up soon.

Issues
----------------
If you have any issues, log them on my github: https://github.com/codyharrington/todolist
