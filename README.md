# Paneity [![Build Status](https://travis-ci.org/reed-college/paneity.svg?branch=master)](https://travis-ci.org/reed-college/paneity)
## Overview

Paniety is a Python based [Django](https://www.djangoproject.com) project developed by the [Reed College Software Design Studio](http://www.reed.edu/sds/). This web application is meant to provide online tutoring to Reed College students. Some of the features include: 
* Instant messaging with tutors
* Forum-style discussion pages
* Search function for finding courses
* Elegant responsive design

Before we get into the setup process, let's talk about some of the Django apps that we used as part of our project.
[Spirit](https://github.com/nitely/Spirit) is a modern Python based forum built on top of Django framework, which we used as a foundation for our forum application. [Django Private Chat](https://github.com/Bearle/django-private-chat) is a Django one-to-one Websocket-based Asyncio-handled chat, developed by Bearle team.

## Setup
Here is how to start running the project!
1. Make a new virtualenv with python 3.6. If you have virtualenvwrapper, you can do this with `mkvirtualenv paneity -p python3`. Afterwords, type `python -V` to make sure you have the right version.
2. Install postgres. If you're on a mac, the easiest way to do that is with the [postgres app.](https://postgresapp.com/)
3. Clone the repo. `git clone git@github.com:reed-college/paneity.git` or `git clone https://github.com/reed-college/paneity.git`
4. Set up spirit. Go out of you paneity directory (`cd ..`) and type `git clone git@github.com:reed-college/Spirit.git`. When you're done, your file structure should look something like this:
```
foldername
├── paneity
│   ├── paneity
│   ├── manage.py
│   └── ...
└── Spirit
    ├── example
    ├── spirit
    └── ...

```
5. install the packages. `cd` into the repo and type `pip install -r requirements.txt`
6. Set up postgres.
    1. Open psql, or if you're in the postgres app click the '⛁' symbol that says 'postgres' below it.
    2. Type the commands on [this page](https://github.com/reed-college/paneity/wiki/Postgres-Set-Up)
7. `python manage.py migrate`
8. `python manage.py collectstatic`. This moves all of the `.css` and `.js` files from their different places in the repo into the `/static/` directory
9. `python manage.py runserver`
10. Go to `localhost:8000` in your browser and there should be something there!
11. In another terminal, activate your virtualenv and in the paniety directory type `python manage.py run_chat_server`. This will let you test out the chat functionality
12. (optional) if you want to put some data in your db, run `python manage.py loaddata subjects courses users questions chats`

## Testing
To run our test suite, use the `python manage.py test tutor` command in the root directory for Paneity.

You should take a look at our [wiki](https://github.com/reed-college/paneity/wiki) for more information.

## Demo Shots
Homepage of Paneity Tutoring Application
![Homepage of Tutoring Application](tutor/static/images/demoshot2.png?raw=true "Paneity Homepage")
Mock-up of Available Tutoring for BIOLOGY 102
![BIOL 102 Tutors](tutor/static/images/demoshot.png?raw=true "Tutoring for Biology 102")


