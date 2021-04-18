import os
import argparse
import pandas as pd
import petl
from datetime import datetime as dt, date
from pdb import set_trace as st
import logging
import psycopg2
from alpaca_trade_api.rest import REST as AlpacaREST, TimeFrame as TF
from .utils import getenv
from .pgutils import get_pg_conn, table_exists

logging.basicConfig(level=logging.INFO)


def get_alpaca_client():
    return AlpacaREST(key_id=getenv('ALPACA_KEY_ID'), 
                      secret_key=getenv('ALPACA_SECRET_KEY'), 
                      base_url=getenv('ALPACA_URL'))


def get_tab_name(ticker, timeframe, sep='_'):
    """Returns Postgres-friendly table name e.g. aapl_1_day"""
    return f"{ticker}{sep}1{sep}{timeframe}".lower()


def get_alpaca_bars(ticker, timeframe, start_date, end_date) -> pd.DataFrame:
    return (get_alpaca_client() 
            .get_bars(
                symbol=ticker, 
                timeframe=getattr(TF, timeframe),
                start=start_date, 
                end=end_date, 
                adjustment='raw')
            .df
            .reset_index()
            .rename(columns=dict(timestamp='time')))


def main(override_db_conn=None, **opts):
    """Main entrypoint function"""
    # pull bars from Alpaca as DataFrame
    df = get_alpaca_bars(**opts)

    # convert types if DB conn override is set
    if override_db_conn is None:
        conn = psycopg2.connect(getenv("DB_URI"))
    else:
        conn = override_db_conn
        df['time'] = df['time'].astype(str)

    # load bars into PostgreSQL DB
    (petl 
     .fromdataframe(df) 
     .appenddb(dbo=conn, 
               tablename=get_tab_name(opts['ticker'], opts['timeframe'])))
    logging.info(f"Successfully loaded data for ticker {opts['ticker']}")


def get_opts():
    """Get command line options from argparse"""
    p = argparse.ArgumentParser(
        description=("Pull historical quotes from Alpaca REST API to "
                     "PostgreSQL DB."))
    p.add_argument('-t', '--ticker', type=str, required=True)
    p.add_argument('-f', '--timeframe', type=str, required=True,
                   choices=['Minute', 'Hour', 'Day'])
    p.add_argument('-s', '--start-date', help='start date', required=True, 
                   type=lambda s: dt.strptime(s, '%Y-%m-%d').date())
    p.add_argument('-e', '--end-date', help='end date', required=False, 
                   type=lambda s: dt.strptime(s, '%Y-%m-%d').date(), 
                   default=dt.today().date())
    return vars(p.parse_args())


if __name__ == '__main__':
    opts = get_opts()
    main(**opts)