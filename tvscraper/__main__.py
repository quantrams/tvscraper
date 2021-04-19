import os
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
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    return chrome_options


def main():
    crawler = TVCrawler(
        # driver=webdriver.Chrome(options=get_chrome_options()), 
        driver_flavor='chrome',
        home_url="https://www.tradingview.com/chart/BCEOOLCE/")
    # crawler = TVCrawler(driver=get_remote_driver())

    crawler.go_home()
    symbols = crawler.get_screener_symbols()


if __name__ == '__main__':
    main()