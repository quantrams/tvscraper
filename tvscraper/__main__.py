from .tv_crawler import TVCrawler


def main():
    crawler = TVCrawler(config_fp="config.yml", secrets_fp="secrets.json")
    # sign if if credentials are available
    if hasattr(crawler, 'secrets'):
        crawler.go("http://www.tradingview.com/#signin")
        crawler.handle_login()
    crawler.go_home()

