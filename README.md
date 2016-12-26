# README #

## Installation ##

Install required packages using [pip](https://pip.pypa.io/en/stable/) (install on [virtualenv](https://virtualenv.pypa.io/en/stable/) is recommended).

In terminal, go to the project directory, run:

    pip install -r requirements.txt

* * *

## Configuration ##

### Database ###

Depend on which [database](https://docs.djangoproject.com/en/1.10/topics/install/#database-installation) used, in **web_django/settings.py**, change `DATABASES` accordingly.

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

### Shop ###
* **Model**: none
* Dashboard for Sgop

### Item ###
* **Model**: Item
* For product page
* Add/edit/delete item (this should be move to Shop package since these actions are in the dashboard)

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
