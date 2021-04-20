# TradingView Scraper

[![Docker publish](https://github.com/quantrams/tvscraper/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/quantrams/tvscraper/actions/workflows/docker-publish.yml)

Scrapes the Screener window for a given [TradingView](http://www.tradingview.com) chart layout.

## Features

- Selenium-chromedriver
- Packaged as executable Docker container for headless execution
    - Parameters passed via argparse
    - Secrets passed via environment variables
- Pytest running in tox, with poetry env support 
- GitHub Actions Docker publish workflow

## Installation

### Poetry

```bash
poetry install
```

### Docker

```bash
docker pull quantrams/tvscraper:latest
```

## Usage

**NOTE**: You will need to create a `.env` file containing TradingView credentials. An [example][1] is provided.

### Python Entrypoint

```bash
source .env
python -m tvscraper --help
```

### Docker

```bash
docker run --env-file .env quantrams/tvscraper:latest --help
```

## Testing

- Run unit tests in tox: `tox --`
    - Requires TV credentials defined in your [`.env`][1]
- Run GitHub Actions pipeline locally using [act](https://github.com/nektos/act)
    ```bash
    act --env-file .env --env DOCKER_USER='my_dockerhub_username' --secret DOCKER_PASSWORD='my_dockerhub_password' push
    ```
- Run tests only (no push) using [act](https://github.com/nektos/act)
    ```bash
    act --env-file .env --env pull_request
    ```

[1]: ./example.env