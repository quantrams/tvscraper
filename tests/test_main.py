import os
import pytest
from alpaca2pg.__main__ import main
from datetime import datetime as dt, date


@pytest.mark.live_db
def test_main(env_context):
    """Runs main entrypoint on live DB."""
    start_date = dt.strptime('2020-10-01', '%Y-%m-%d').date()
    end_date = dt.strptime('2021-01-01', '%Y-%m-%d').date()
    ticker = 'AAPL'
    result = main(
        ticker=ticker, start_date=start_date, end_date=end_date,
        timeframe='Day'
    )


def test_on_sqlite(env_context, sqlite_tab):
    """Runs main entrypoint on sqlite in-memory."""
    # create empty table, returning sqlite connection
    conn = sqlite_tab('aapl_1_day')

    start_date = dt.strptime('2020-10-01', '%Y-%m-%d').date()
    end_date = dt.strptime('2021-01-01', '%Y-%m-%d').date()
    ticker = 'AAPL'
    result = main(
        ticker=ticker, start_date=start_date, end_date=end_date,
        timeframe='Day',
        override_db_conn=conn
    )