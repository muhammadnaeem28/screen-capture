import pytest
from os.path import dirname
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope='module', autouse=False)
def b2b_config(configs, service_configs):
    b2b_dir_path = dirname(__file__)
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')

    b2b_config = {
        "browser": webdriver.Chrome("/usr/bin/chromedriver", options=options),
        "username": service_configs["username"],
        "password": service_configs["password"],
        "base_url": service_configs["base_url"],
        "b2b_dir_path": b2b_dir_path
    }

    return b2b_config
