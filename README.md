# Argstore (stands for args store)

[![Argstore](https://github.com/fleshofcat/argstore/actions/workflows/ci_cd.yaml/badge.svg)](https://github.com/fleshofcat/argstore/actions/workflows/ci_cd.yaml)
![Coverage badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/fleshofcat/d01bb46aff24caedfa24f12d77fd3f42/raw/argstore__master.json)

This is a simple REST API for storing named strings as user parameters.
Users in this system are just entities in the database, without registration or anything else.

The initial technical requirements for this project were the following API, which this service implements:

![Required API](doc/required_api.png)

A user API for testing the project has also been implemented:

(There is no update user endpoint because there are no updateable fields in users in this version)

![Users API](doc/users_api.png)

---------

This projects uses poetry as a package manager, so [install it.](https://python-poetry.org/docs/#installation)

## Run with docker

``` bash
# Create db/argstore.db
docker run -it -p 8000:8000 -e SQLALCHEMY_DATABASE_URL=sqlite:////app/db/argstore.db -v /path/to/your/db/:/app/db argstore:latest
```

## For developers

After getting the source code install the pre-commit hooks for automate code checking.

``` bash
poetry run pre-commit install -t=pre-commit -t=pre-push
```
