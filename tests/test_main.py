import os
import pytest
from tvscraper.__main__ import main
from datetime import datetime as dt, date


def test_main(env_context):
    opts = {
        'url': "https://www.tradingview.com/chart/OkjDZr3W/"
    }
    main(**opts)