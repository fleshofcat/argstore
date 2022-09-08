# Argstore (stands for args store)

[![Argstore](https://github.com/fleshofcat/argstore/actions/workflows/ci.yaml/badge.svg)](https://github.com/fleshofcat/argstore/actions/workflows/ci.yaml)
![Coverage badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/fleshofcat/d01bb46aff24caedfa24f12d77fd3f42/raw/argstore__master.json)

This is a simple REST API for storing named strings as parameters.

This projects uses poetry as a package manager, so [install it.](https://python-poetry.org/docs/#installation)

## For developers

After getting the source code install the pre-commit hooks for automate code checking.

``` bash
poetry run pre-commit install -t=pre-commit -t=pre-push
```
