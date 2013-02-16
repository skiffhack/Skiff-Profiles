SkiffHack
---------




Installation
============


To clone the repo::

    git clone git@github.com:skiffhack/Skiff-Profiles.git

To setup::

    virtualenv --no-site-packages --distribute --python=python2.6 env
    source env/bin/activate
    pip install -r requirements.txt
    python settings/secrets_template.py  # Get a new secret key
    # Create settings/secret.py and add "SECRET_KEY = {generated secret key}"

To run the project::
    

    source env/bin/activate
    manage.py syncdb
    manage.py migrate
    manage.py runserver

To run the tests::

    manage.py test


Database Migrations
===================

Check out the South [documentation](http://south.aeracode.org/docs/) and [tutorial](http://south.aeracode.org/docs/tutorial/index.html)

To create a new migration after changing models.py::

    manage.py schemamigration assetcloud --auto

To apply new migrations::

    manage.py migrate assetcloud

To list all migrations (and see which have not yet been applied)::

    manage.py migrate --list

Templates
=========

Templates are based on [Twitter Bootstrap](http://twitter.github.com/bootstrap/).
