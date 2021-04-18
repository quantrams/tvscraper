import os
import pytest
from tvscraper.__main__ import main
from datetime import datetime as dt, date


def test_main(env_context):
    main()