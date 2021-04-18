# alpaca2pg

Loads data from an [Alpaca v1 API](https://github.com/alpacahq/alpaca-trade-api-python) query to a PostgreSQL database. 

## Features

- Python package via [poetry](https://python-poetry.org/)
- Packaged as executable Docker container
    - Parameters passed via argparse
    - Secrets passed via environment variables
- Pytest running in tox, with poetry env support and local SQLite3 fixture
- GitHub Actions Docker publish workflow

## Installation

### Poetry

```bash
poetry install
```

### pip

```bash
pip install -r requirements.txt
pip install .
```

### Docker

```bash
docker pull quantrams/alpaca2pg:latest
```

## Usage

**NOTE**: You will need to create a `.env` file containing database and Alpaca credentials. An [example][1] is provided.

### Python Entrypoint

```bash
source .env
python -m alpaca2pg --help
```

### Docker

```bash
docker run --env-file .env quantrams/alpaca2pg:latest --help
```

## Testing

- Run unit tests with a live DB connection: `tox --`
    - Requires `DB_URI` defined in your [`.env`][1]
- Run unit tests using a SQLite3 fixture: `tox -- -m 'not live_db'`
    - Requires only Alpaca credentials defined in your [`.env`][1]
- Run GitHub Actions pipeline locally using [act](https://github.com/nektos/act)
    ```bash
    act --env DOCKER_USER='my_dockerhub_username' --secret DOCKER_PASSWORD='my_dockerhub_password' push`
    ```
- Run tests only (no push) using [act](https://github.com/nektos/act)
    ```bash
    act pull_request`
    ```

[1]: ./example.env