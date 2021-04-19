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
    # chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_prefs = dict()
    # chrome_options.experimental_options["prefs"] = chrome_prefs
    # chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options


def main():
    crawler = TVCrawler(driver=webdriver.Chrome(options=get_chrome_options()))
    # crawler = TVCrawler(driver=get_remote_driver())
    # sign if if credentials are available
    if hasattr(crawler, 'secrets'):
        crawler.go("http://www.tradingview.com/#signin")
        crawler.handle_login()
    crawler.go_home()
    print("URL is :", crawler.driver.current_url)

if __name__ == '__main__':
    main()