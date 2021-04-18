import json
import os
import random
import logging
from time import sleep


def rand_wait(before: list = [1, 3], after: list = None, verbose=True):
    """Decorator factory. Only works with methods."""
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            # before sleep
            _before = getattr(self, 'rand_wait_before', before)
            before_int = random.uniform(*_before)
            if verbose is True:
                logging.debug(f"Sleeping {before_int:.2f} seconds before function '{func.__name__}'")
            sleep(before_int)

            return_val = func(self, *args, **kwargs)

            # after sleep
            _after = getattr(self, 'rand_wait_after', after)
            if _after is not None:
                after_int = random.uniform(*_after)
                if verbose is True:
                    logging.debug(f"Sleeping {after_int:.2f} seconds after function '{func.__name__}'")
                sleep(after_int)
            return return_val
        return wrapper
    return decorator


def wait(before, after=0, verbose=True):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if verbose is True:
                logging.debug(f"Sleeping {before:.2f} seconds before function '{func.__name__}'")
            sleep(before)
            return_val = func(*args, **kwargs)
            if after > 0:
                if verbose is True:
                    logging.debug(f"Sleeping {after:.2f} seconds before function '{func.__name__}'")
                sleep(after)
            return return_val
        return wrapper
    return decorator


def icontains(text, query) -> bool:
    assert isinstance(text, str)
    assert isinstance(query, str)
    return query.lower().strip() in text.lower().strip()


def get_bot_token():
    action_list = [
        (get_bot_token_from_secrets, FileNotFoundError, 'Failed to find token in JSON file'),
        (get_bot_token_from_env, KeyError, 'Failed to get token from env'),
    ]
    for action, ex, msg in action_list:
        try:
            return action()
            break
        except ex as _err:
            print(msg)
            err = _err
            continue
    raise err


def get_bot_token_from_secrets(field_name='BOT_TOKEN',
                               secrets_fp='secrets.json') -> str:
    with open(secrets_fp) as f:
        data = json.load(f)
    assert field_name in data
    return data[field_name]


def get_bot_token_from_env(env_name='BOT_TOKEN') -> str:
    return os.environ[env_name]
