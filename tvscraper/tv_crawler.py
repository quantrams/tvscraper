from time import sleep
import logging
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from .base_crawler import BaseCrawler
from .utils import wait
from selenium.common.exceptions import ElementClickInterceptedException


class TVCrawler(BaseCrawler):
    HOME_URL = "http://www.tradingview.com/chart"
    OHLC_XPATH = ("/html/body//div[contains(@class,'valueItem')]/"
                  "div[contains(text(),'{0}')]/../div[2]")
    SCREENER_SYMS_XPATH = ("/html/body//div[contains(@class, 'tv-screener')]" 
                           "//table/tbody//td[1]//div[@title]")

    def get_xpath(self, name):
        if name in 'ohlc':
            return self.OHLC_XPATH.format(name.upper())
        else:
            raise NotImplementedError(name)

    def get_ohlc_from_price_bar(self) -> dict:
        d = dict()
        for name in 'ohlc':
            xpath = self.get_xpath(name)
            value = self.driver.find_element_by_xpath(xpath).text
            d[name] = float(value)
        return d

    def get_ohlc(self, how='price_bar'):
        if how == 'price_bar':
            return self.get_ohlc_from_price_bar()
        else:
            raise NotImplementedError(how)

    # we need a tiny pause before updating price
    @wait(0, after=0.2)
    def next_bar(self):
        webdriver.ActionChains(self.driver).key_down(
            Keys.SHIFT).send_keys(Keys.RIGHT).perform()

    def toggle_replay(self):
        raise NotImplementedError()
        webdriver.ActionChains(self.driver).key_down(
            Keys.SHIFT).send_keys(Keys.DOWN).perform()

    def get_ticker(self):
        return self.driver.find_element_by_xpath(
            "/html/body//div[@data-role='button' and contains(@id, 'symbol')]"
        ).text

    @wait(1)
    def handle_login(self):
        email_button = self.driver.find_element_by_xpath(
            "/html/body//span[contains(text(), 'Email')]"
        )
        self.click(email_button)
        user_box = self.driver.find_element_by_xpath(
            "/html/body//input[contains(@name, 'username')]")
        pass_box = self.driver.find_element_by_xpath(
            "/html/body//input[contains(@name, 'password')]")
        submit = self.driver.find_element_by_xpath(
            "/html/body//button[@type='submit']")
        user_box.send_keys(self.secrets.TV_USER)
        pass_box.send_keys(self.secrets.TV_PASS)
        self.click(submit)

    @wait(10)
    def get_screener_symbols(self):
        export_button = self.driver.find_element_by_xpath(
            "/html/body//div[contains(@class, 'tv-screener-toolbar') "
            "and contains(@data-name, 'export')]"
        )
        sleep(3)
        try:
            logging.debug(f"Attemping export...")
            export_button.click()
        except ElementClickInterceptedException:
            self.driver.find_element_by_xpath(
                "/html/body//*[@data-name='close']").click()
            sleep(3)
            export_button.click()
        sleep(20)
        logging.debug(f"Finished method get_screener_symbols")
        
        