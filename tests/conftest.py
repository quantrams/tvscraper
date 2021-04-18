import os
import pytest
import psycopg2
import sqlite3
from dotenv import dotenv_values


@pytest.fixture
def dot_env() -> dict:
    """.env by default"""
    return dotenv_values()


@pytest.fixture
def env_context(dot_env, monkeypatch):
    """Get env file .env"""
    for k, v in dot_env.items():
        monkeypatch.setenv(k, v)
        # DEBUG
        # print(f'setting {k} to {v}')


@pytest.fixture
def sqlite_conn():
    """Fixture to set up the in-memory database with test data."""
    conn = sqlite3.connect(':memory:')
    yield conn
    conn.close()
    

@pytest.fixture
def sqlite_tab(sqlite_conn):
    """Factory that creates empty table with `tab_name` from sqlite connection."""
    def create_tab(tab_name):
        cursor = sqlite_conn.cursor()
        cursor.execute('''CREATE TABLE aapl_1_day( 
                    time TEXT, 
                    open REAL, 
                    high REAL, 
                    low REAL, 
                    close REAL, 
                    volume REAL)''')
        return sqlite_conn
    return create_tab


@pytest.fixture
def pg_conn(env_context):
    """Connect to PostgreSQL DB using URI in .env file"""
    uri = os.getenv('DB_URI')
    assert uri is not None
    conn = psycopg2.connect(uri)
    yield conn
    conn.close()
