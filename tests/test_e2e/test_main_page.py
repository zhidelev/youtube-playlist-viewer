def test_main_page(browser):
    page = browser.new_page()
    page.goto("http://localhost:3000")
    assert page.title() == "Recommended videos"
