import pytest

from playwright.sync_api import sync_playwright


@pytest.fixture(scope="session")
def browser():
    """
    Returns an instance of Chromium.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()

        yield browser

        browser.close()
