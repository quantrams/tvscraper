import os
import psycopg2
import pkg_resources
from .utils import getenv


def get_pg_uri(user, password, host, port, dbname) -> str:
    """Returns PostgreSQL URI-formatted string."""
    return f'postgresql://{user}:{password}@{host}:{port}/{dbname}'


def get_pg_conn():
    """Connect to remote DB using credentials in env"""
    kw = {k: getenv(f"PG_{k.upper()}") for k in 
          ('dbname', 'user', 'password', 'host', 'port')}
    uri = get_pg_uri(**kw)
    return psycopg2.connect(uri)


def get_sql(fname, sql_dir='sql', pkg_name='alpaca2pg') -> str:
    """Reads SQL query from file at `sql_dir`/`fname`."""
    fp = pkg_resources.resource_filename(pkg_name, os.path.join(sql_dir, fname))
    with open(fp, 'r', encoding='utf-8') as f:
        return f.read()


def table_exists(cur, tab_name) -> bool:
    cur.execute(get_sql('table_exists.sql'), (tab_name,))
    return bool(cur.fetchone()[0])


