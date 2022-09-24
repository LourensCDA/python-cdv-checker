Project to run a bank account algorithm check (CDV).

## Pipenv

Pipenv is a virtual enviroment, it makes it easy to record your dependencies.

For more info see: [https://pypi.org/project/pipenv/](https://pypi.org/project/pipenv/)

To install:

```ps
pip install pipenv
```

To install dependencies, in the directory run:

```ps
pipenv install
```

To run:

```ps
pipenv run python db_setup.py
```

## Dockerfile

You can create a docker image of this using the following commands:

```ps
docker build -t python-cdv
```

To run:

```ps
docker run -it python-cdv
```

## Waht am I using?

- Python 3.10
- SQLite3
