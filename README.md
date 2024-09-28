# Project Name

A comprehensive guide to setting up and running the project using Docker, Django, MariaDB/MySQL, and Redis. This project is optimized for Linux environments or Windows with WSL (Windows Subsystem for Linux).

## Table of Contents

- [Prerequisites](#prerequisites)
- [Project Setup](#project-setup)
  - [Setting enviromental variables](#setting-enviromental-variables)
  - [Creating Essential Directories](#creating-essential-directories)
  - [Initializing the Django Project](#initializing-the-django-project)
  - [Setting Permissions](#setting-permissions)
- [Managing Docker Containers](#managing-docker-containers)
  - [Stopping Containers](#stopping-containers)
  - [Starting Containers](#starting-containers)
- [Additional Information](#additional-information)

## Prerequisites

- **Operating System**: Linux or Windows with WSL
- **Docker**: Ensure Docker and Docker Compose are installed
- **Python**: Django requires Python; make sure it's installed within your Docker environment

## Project Setup

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



## Additional Information

Environment Variables: Ensure that your .env file contains the necessary environment variables for database and Redis configurations, such as MYSQL_DATABASE, MYSQL_USER, MYSQL_PASSWORD, REDIS_PASSWORD, WEB_PORT, and REDIS_COMMANDER_PORT.

Docker Compose: Customize your docker-compose.yml as needed to fit the project requirements, including service definitions for Django, MariaDB/MySQL, and Redis.

Further Development: Explore adding more Django apps, APIs with Django REST Framework, and front-end frameworks as your project evolves.

