import os
from glob import glob
import argparse
import pathlib
from attrdict import AttrDict
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from .tv_crawler import TVCrawler

DL_DIR = "/tmp/chrome_downloads"


def get_remote_driver(url="http://localhost:4444/wd/hub"):
    return webdriver.Remote(url, DesiredCapabilities.CHROME)


def get_chrome_options():
    """Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """
    # mkdir -p
    pathlib.Path(DL_DIR).mkdir(parents=True, exist_ok=True)

    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": DL_DIR,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    return chrome_options


def main(**opts):
    crawler = TVCrawler(
        driver=webdriver.Chrome(options=get_chrome_options()), 
        # driver_flavor='chrome',
        # driver=get_remote_driver()
        home_url=opts['url'])

    # enter TradingView credentials
    crawler.secrets = AttrDict({k: os.environ[k] for k in ('TV_USER', 'TV_PASS')})

    # handle login
    crawler.go("http://www.tradingview.com/#signin")
    crawler.handle_login()

    # go to screener window and download
    crawler.go_home()
    symbols = crawler.get_screener_symbols()

    if opts['cat_symbols']:
        cat_csvs()


def cat_csvs():
    fps = glob(os.path.join(DL_DIR, '*.csv'))
    assert fps, f"no CSV files found in {DL_DIR}"
    for fp in fps:
        with open(fp, 'r') as f:
            print(f.read())


def get_opts():
    """Get command line options from argparse"""
    p = argparse.ArgumentParser(
        description="Scrape TradingView Screener for a given chart")
    p.add_argument('-u', '--url', type=str, required=False,
                   default="https://www.tradingview.com/chart/OkjDZr3W/")
    p.add_argument('--cat-symbols', action='store_true', required=False,
                   default=True)
    return vars(p.parse_args())


if __name__ == '__main__':
    opts = get_opts()
    main(**opts)