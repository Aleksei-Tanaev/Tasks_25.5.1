import pytest
from selenium.webdriver import Chrome

from settings import path_driver


@pytest.fixture
def chrome_options(chrome_options):
    #chrome_options.add_argument('--kiosk')
    chrome_options.set_headless(True)
    return chrome_options


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = Chrome(path_driver)
    pytest.driver.maximize_window()

    yield pytest

    pytest.driver.quit()



