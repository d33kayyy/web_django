# README #

## Installation ##

Install required packages using [pip](https://pip.pypa.io/en/stable/) (install on [virtualenv](https://virtualenv.pypa.io/en/stable/) is recommended).

In terminal, go to the project directory (eg: `cd PycharmProjects/silisili-web/`), run:

    pip install -r requirements.txt

* * *

## Configuration ##

### Database ###

* **Config**

    Depend on which [database](https://docs.djangoproject.com/en/1.10/topics/install/#database-installation) used, in **silisili/settings.py**, change `DATABASES` accordingly. Example using SQLite:

        DATABASES = {
           'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
           }
        }

    or using Postgresql

        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': 'postgres',
                'USER': 'dk',
                'PASSWORD': '1',
                'HOST': '127.0.0.1',
                'PORT': '5432',
            }
        }

* **Migrate**

    To migrate data, run:

        python manage.py migrate


### Extra configurations (for first time only) ###

Create superuser (admin) in order to login to admin page, run:

    python manage.py createsuperuser

After create admin account, loginto admin page (eg: `localhost:8000/admin`):

* Find **Sites**, go into that and change to **your domain name and display name**. For local testing only:

        localhost:8000
        SiliSili

* Back to admin homepage, find **Social applications** then add your Social App, more information can be found [here](http://django-allauth.readthedocs.io/en/latest/providers.html):

        These are Kien's registered apps for local testing only, create new apps for deployment. Follow link above for more information

        Google App:
            * Provider: Google
            * Client id = 30365204598-vsk8l9ebs3tes590tgn3lf37ji3vl2bb.apps.googleusercontent.com
            * Secret key = aje8P3fL8BBENZqpGKAthSyK
            * Add your site into "Chosen sites"


        Facebook App
            * Provider: Facebook
            * Client id = 1735709893344808
            * Secret key = a764d464bd8609806cf0d93275007bf0
            * Add your site into "Chosen sites"

### Note ###

After installation, when start server and the error below occurs, follow [this](https://github.com/justquick/django-activity-stream/issues/308) :

    File "/home/dk/.virtualenv/env/lib/python3.5/site-packages/actstream/urls.py", line 5, in <module>
        from django.conf.urls.defaults import url, patterns
    ImportError: No module named 'django.conf.urls.defaults'

* * *

## Libraries ##

* **[django-allauth](http://django-allauth.readthedocs.io/en/latest/index.html)**
    + django-bootstrap-form
* **[django-activity-stream](http://django-activity-stream.readthedocs.io/en/latest/)**
    + django-jsonfield
    + django-model-utils
* **[django-notifications-hq](https://github.com/django-notifications/django-notifications)**
* **[django-widget-tweaks](https://github.com/kmike/django-widget-tweaks/)**

* * *

## Project Structure ##

### Users ###
* **Model**: User, UserProfile
* Handle user signup/login, populate UserProfile
* Activity log (notification list)

### Chef ###
* **Model**: none
* Dashboard for chef

### Item ###
* **Model**: Item
* For product page
* Add/edit/delete item (this should be move to Chef package since these actions are in the dashboard)

### Cart ###
* **Model**: none
* Handle add/remove/update item from cart
* Information and confirmation during transaction
* Create Order and ItemOrder at the end of transaction

### Order ###
* **Model**: Order, ItemOrder
* Creation of orders and items in order.
* Order history page

### Reviews ###
* **Model**: Review
* Review page and handle review creation
