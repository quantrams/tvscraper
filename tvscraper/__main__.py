import os
import argparse
import pathlib
from attrdict import AttrDict
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from .tv_crawler import TVCrawler


def get_remote_driver(url="http://localhost:4444/wd/hub"):
    return webdriver.Remote(url, DesiredCapabilities.CHROME)


def get_chrome_options():
    """Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """
    dl_dir = "/tmp/chrome_downloads"
    # mkdir -p
    pathlib.Path(dl_dir).mkdir(parents=True, exist_ok=True)

    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": dl_dir,
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


def get_opts():
    """Get command line options from argparse"""
    p = argparse.ArgumentParser(
        description="Scrape TradingView Screener for a given chart")
    p.add_argument('-u', '--url', type=str, required=True,
                   default="https://www.tradingview.com/chart/BCEOOLCE/")
    return vars(p.parse_args())


if __name__ == '__main__':
    opts = get_opts()
    main(**opts)