import logging
import random
import yaml
import json
from attrdict import AttrDict
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.remote.remote_connection import LOGGER
from .utils import icontains, wait, rand_wait

LOGGER.setLevel(logging.WARNING)


class BaseCrawler(object):
    BUTTON_XPATH = "//button"
    INPUT_XPATH = "//input"
    HOME_URL = "https://www.google.com"

    # Format is (name, type, default, required)
    # None is valid for type or default
    INIT_KWARGS = (
        # Included implicitly
        # ("config", AttrDict, None, False),
        # ("config_fp", str, None, False),
        ("driver", None, None, False),
        ("driver_flavor", str, "chrome", False),
        ("home_url", str, HOME_URL, True),
        ("button_xpath", str, BUTTON_XPATH, True),
        ("input_xpath", str, INPUT_XPATH, True),
        ("rand_wait_before", list, [0, 0], True),
        ("rand_wait_after", list, [0, 0], True),
    )

    def __init__(self, *args, **kwargs):

        # Try to load a config
        if kwargs.get('config') is not None:
            assert isinstance(kwargs['config'], AttrDict)
            self.config = kwargs['config']
        elif kwargs.get('config_fp') is not None:
            assert isinstance(kwargs['config_fp'], str)
            self.config = self.get_config(kwargs['config_fp'])

        # Try to load a secrets file
        if kwargs.get('secrets') is not None:
            assert isinstance(kwargs['secrets'], AttrDict)
            self.secrets = kwargs['secrets']
        elif kwargs.get('secrets_fp') is not None:
            assert isinstance(kwargs['secrets_fp'], str)
            self.secrets = self.get_secrets(kwargs['secrets_fp'])

        # Passing kwargsargs overwrites secrets, which overwrites config
        kw = getattr(self, 'config', dict())
        kw.update(getattr(self, 'secrets', dict()))
        kw.update(kwargs)

        # Enforce config/secrets/kwargs and load defaults
        for (name, ty, default, req) in self.INIT_KWARGS:
            # populate defaults
            if name not in kw:
                if req is True:
                    if default is None:
                        raise ValueError(
                            f"Kwarg '{name}' is required but was not passed " +
                            "to constructor or found in config.")
                    else:
                        kw[name] = default
                else:
                    continue
            # type check
            if ty is not None and not isinstance(kw[name], ty):
                raise TypeError(f"Kwarg '{name}' was passed but is not the right " +
                                "type. Expected '{ty.__name__}', got '{type(kw[name])}'")
            # setattr
            if hasattr(self, name):
                raise ValueError(f"Attempted to set attribute named " +
                                 f"'{name}', but it already exists.")
            else:
                setattr(self, name, kw[name])

        # Get a driver
        if kw.get('driver') is not None:
            self.driver = kw['driver']
        elif kw.get('driver_flavor') is not None:
            self.driver = self.get_driver(flavor=kw['driver_flavor'])
        else:
            raise ValueError("Please supply either 'driver' or 'driver_flavor' kwarg")

    def get_config(self, config_fp) -> AttrDict:
        """Reads a YAML file at `config_fp` and returns contents as AttrDict."""
        with open(config_fp, 'r') as f:
            data = yaml.safe_load(f)
        return AttrDict(data)

    def get_secrets(self, secrets_fp='./secrets.json') -> AttrDict:
        """Reads a YAML file at `secrets_fp` and returns contents as AttrDict."""
        with open(secrets_fp, 'r') as f:
            data = json.load(f)
        return AttrDict(data)

    @wait(0, 3)
    def go(self, url):
        self.driver.get(url)

    def go_home(self):
        self.go(self.home_url)

    @rand_wait()
    def find_element_by_text(self, elems, query, assert_one=True):
        assert isinstance(elems, list)
        assert len(elems) != 0
        matches = [e for e in elems if icontains(e.text, query)]
        if len(matches) == 0:
            raise ValueError(f"No matches ({len(matches)}) found for " +
                             f"text query '{query}'")
        elif assert_one is True and len(matches) > 1:
            raise ValueError(f"Too many matches ({len(matches)}) found for " +
                             f"text query '{query}'")
        else:
            return matches[0]

    @rand_wait()
    def click_at_loc(self, elem, offset: list = [10, 5],
                     x_jitter: list = [-7, 5], y_jitter: list = [-3, 3]):
        # get random x and y offset
        dx = random.uniform(*x_jitter)
        dy = random.uniform(*y_jitter)
        offset = [offset[0] + dx, offset[1] + dy]

        action = webdriver.common.action_chains.ActionChains(self.driver)
        action.move_to_element_with_offset(elem, *offset)
        action.click()
        action.perform()

    @wait(1, 1)
    def click(self, elem, intercept_retry=0):
        try:
            elem.click()
        except ElementClickInterceptedException:
            # click anyway, with retries
            if intercept_retry == 0:
                raise
            logging.info(f"Another element intercepted click. Trying click " +
                         f"{intercept_retry} more times until we change URL...")
            # keep clicking until we run out of tries or the URL changes
            og_url = self.driver.current_url
            for _ in range(intercept_retry + 1):
                if self.url_has_changed(og_url):
                    break
                else:
                    self.click_at_loc(elem)

    def click_button(self, query: str, xpath: str = None, assert_one=True):
        if xpath is None:
            xpath = self.button_xpath
        buttons = self.driver.find_elements_by_xpath(xpath)
        self.click(
            self.find_element_by_text(buttons, query, assert_one=assert_one),
            intercept_retry=3
        )

    @rand_wait()
    def fill_input(self, text: str, xpath: str = None):
        if xpath is None:
            xpath = self.input_xpath
        raise NotImplementedError()

    def url_has_changed(self, og_url):
        """Has the URL changed from `og_url`?
        TODO: less strict URL parsing
        """
        return og_url != self.driver.current_url

    def get_chrome_options(self, *args):
        opts = Options()
        opts.add_argument(*args)
        return opts

    def get_chrome_driver(self):
        return webdriver.Chrome(
            chrome_options=self.get_chrome_options("--window-size=1500,1000"),
            executable_path="chromedriver"
        )

    def get_driver(self, flavor='chrome'):
        if flavor == 'chrome':
            return self.get_chrome_driver()
        else:
            raise ValueError("Please supply a valid driver flavor")
