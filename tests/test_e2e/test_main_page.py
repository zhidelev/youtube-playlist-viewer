def test_main_page(browser):
    page = browser.new_page()
    page.goto("http://localhost:8000")
    assert page.title() == "Recommended videos"
