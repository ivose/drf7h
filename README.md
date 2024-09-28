# Project Name

A comprehensive guide to setting up and running the project using Docker, Django, MariaDB/MySQL, and Redis. This project is optimized for Linux environments or Windows with WSL (Windows Subsystem for Linux).

## Table of Contents

- [Prerequisites](#prerequisites)
- [Project Setup](#project-setup)
  - [Setting a prefix](#setting-a-prefix)
  - [Setting enviromental variables](#setting-enviromental-variables)
  - [Creating Essential Directories](#creating-essential-directories)
  - [Initializing the Django Project](#initializing-the-django-project)
  - [Setting Permissions](#setting-permissions)
- [Managing Docker Containers](#managing-docker-containers)
  - [Stopping Containers](#stopping-containers)
  - [Starting Containers](#starting-containers)
- [Configuring Django Settings](#configuring-django-settings)
  - [Basic Configuration](#basic-configuration)
  - [Database Configuration](#database-configuration)
  - [Redis Caching Configuration](#redis-caching-configuration)
- [Implementing Redis Demo](#implementing-redis-demo)
  - [Creating the View](#creating-the-view)
  - [Updating URLs](#updating-urls)
- [Static Files and Front-end Setup](#static-files-and-front-end-setup)
- [Testing the Setup](#testing-the-setup)
- [Additional Information](#additional-information)

## Prerequisites

- **Operating System**: Linux or Windows with WSL
- **Docker**: Ensure Docker and Docker Compose are installed
- **Python**: Django requires Python; make sure it's installed within your Docker environment

## Project Setup

### Setting a prefix

I'd like recommend to use a prefix, especially if you've several docker-projects in your server. Currently here is used 'mypref-' that for example in VS Code use Ctrl+Shift+H for replacing it with your own prefix in every file where is represented.

### Setting enviromental variables

Create file '.env' and copy the content of '.env.sample' to it or rename the '.env.sample' to '.env'. After then replace values as you want.

### Creating Essential Directories

Start by creating the necessary directories for the project. Open your terminal and execute the following commands:

```bash
mkdir data
mkdir pr
```

### Initializing the Django Project

Use Docker Compose to run the Django admin command and initialize the project within the pr directory.

```bash
docker compose run mypref-web django-admin startproject pr .
```


### Setting Permissions

Ensure that the source code directory is owned by your user to allow for editing.

```bash
sudo chown -R $USER:$USER ./pr
```

#### Creating an app inside project

For creating app (e.g with name base) with a command e.g 'python manage.py startapp base' use

```bash
docker compose run mypref-web python manage.py startapp base
```

And after this set the permissions of the files, that you can edit the files:


```bash
sudo chown -R $USER:$USER ./pr/base
```

or 

```bash
sudo chown -R $USER:$USER ./pr
```

The permissions has to set always after creating folders or files with docker.

If you have the same version of the python also in your so called mother operationg system, than you can use also

```bash
python manage.py startapp base
```
or 
```bash
python3 manage.py startapp base
```

Commonly this action must use also in other manage.py commands for creating different things. For example makemigrations and migrate for supplementing database. And updating database (e.g migrate or createrootuser) is needed trough docker.

## Managing Docker Containers

### Stopping Containers

To temporarily stop all running containers, use:

```bash
docker-compose down
```

### Starting Containers

Start the containers in detached mode, rebuild if necessary, and remove any orphaned containers:

```bash
docker-compose up -d --build --remove-orphans
```

'--build' means, it builds the docker-container again. '--remove-orphans' Removes any containers that were started by previous versions of the docker-compose.yml file but are no longer defined in the current file, it avoids creating a large number of 'none' containers.

## Configuring Django Settings

### Basic Configuration

Edit the pr/pr/settings.py file to adjust the basic settings.

#### 1. Import OS Module

At the beginning of the file, add:

```python
import os
```

#### 2. Allowed Hosts

Change the ALLOWED_HOSTS setting to allow all hosts:

```python
ALLOWED_HOSTS = ['*']
```
or only desired hosts

```python
ALLOWED_HOSTS = ['yourdomain.com', 'localhost']
```

#### 3. Installed Apps

Add rest_framework and django_redis to the INSTALLED_APPS list if you're building an API project:

```python
INSTALLED_APPS = [
    # ... existing apps ...
    'django_redis',
    'rest_framework',
]
```

### Database Configuration

If you prefer using MariaDB/MySQL over SQLite, modify the DATABASES setting in the same settings.py file as follows:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('MYSQL_DATABASE'),
        'USER': os.environ.get('MYSQL_USER'),
        'PASSWORD': os.environ.get('MYSQL_PASSWORD'),
        'HOST': 'mypref-mariadb',
        'PORT': 3306,
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}
```

### Redis Caching Configuration

To utilize Redis for caching, append the following configuration after the DATABASES setting:

```python
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/0",  # 'redis' is the hostname defined in docker-compose.yml
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', '')
if REDIS_PASSWORD:
    CACHES["default"]["OPTIONS"]["PASSWORD"] = REDIS_PASSWORD
    CELERY_BROKER_URL = f'redis://:{REDIS_PASSWORD}@redis:6379/0'
else:
    CELERY_BROKER_URL = 'redis://redis:6379/0'

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
```

## Implementing Redis Demo

### Creating the View

Create a demo view to test Redis functionality. Add the following code to pr/pr/views.py:

```python
from django.core.cache import cache
from django.http import HttpResponse
from django_redis import get_redis_connection
import datetime

def redis_demo(request):
    # Using Django's cache framework
    now = datetime.datetime.now()
    if not cache.get('my_key'):
        cache.set('my_key', f'Hello, Redis! {now}', timeout=60)  # Expires in 60 seconds
    redis_conn = get_redis_connection("default")

    # Uncomment one of the following lines to test different Redis operations
    # redis_conn.set('my_direct_key', 'Hello from Redis client!')
    direct_value = redis_conn.get('my_direct_key')
    # redis_conn.delete('my_direct_key')

    response = (
        f"<h2>Using Django's cache framework:</h2>"
        f"Value of cache['my_key']: {cache.get('my_key')}<br>"
        f"<h2>Using Redis client directly:</h2>"
        f"Value: {direct_value}"
    )

    return HttpResponse(response)
```

### Updating URLs

Integrate the redis_demo view into your URL configuration.

#### 1. Import the View

At the top of pr/pr/urls.py, add:

```python
from . import views
```

#### 2. Add URL Pattern

Within the urlpatterns list, include the new path:

```python
urlpatterns = [
    # ... existing paths ...
    path('redis/', views.redis_demo, name='redis_demo'),
]
```



## Static Files and Front-end Setup

To serve static files such as JavaScript, images, and CSS, update the static settings in pr/pr/settings.py:

```python
STATIC_URL = '/static/'

# Add these new lines
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```
or
```python
STATIC_URL = '/static/'

# Add these new lines
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```


##### Example

Create a JavaScript file named app.js inside the static directory. It will be accessible via:

```bash
http://localhost:<WEB_PORT>/static/app.js
```

Replace <WEB_PORT> with the port number specified in your .env file (e.g., WEB_PORT=8000).

## Testing the Setup

#### 1. Access the Redis Demo
Navigate to:

```bash
http://localhost:8000/redis/
```

You should see the output from both Django's cache framework and the direct Redis client.

#### 2. Access Redis Commander

If you have Redis Commander set up, access it via:

```bash
http://localhost:8082
```

#### 3. Verify Static Files

Create a file app.js into pr/static and access your JavaScript file to ensure static files are served correctly:

http://localhost:8000/static/app.js


## Additional Information

Environment Variables: Ensure that your .env file contains the necessary environment variables for database and Redis configurations, such as MYSQL_DATABASE, MYSQL_USER, MYSQL_PASSWORD, REDIS_PASSWORD, WEB_PORT, and REDIS_COMMANDER_PORT.

Docker Compose: Customize your docker-compose.yml as needed to fit the project requirements, including service definitions for Django, MariaDB/MySQL, and Redis.

Further Development: Explore adding more Django apps, APIs with Django REST Framework, and front-end frameworks as your project evolves.

