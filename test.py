from time import sleep
from playwright.sync_api import Playwright, sync_playwright, expect


def buy_product(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    # Open new page
    page = context.new_page()

    # Go to https://www.nike.com/gb/launch/t/womens-air-max-97-gorge-green
    page.goto('https://www.nike.com/gb/launch/r/DV2635-400')
    page.mouse.wheel(0,500)
    # Click text=UK 13
    sizes = page.query_selector_all(selector='button[class="size-grid-dropdown size-grid-button"]')
    if len(sizes) == 0:
        for i in range(len(sizes)):
            print(f'[{i}]->{sizes[i].inner_html()}')
        user_choice = int(input('Enter the size you want to choose you have to type the index number : '))
        try:
            sizes[user_choice].click()
            
            page.mouse.wheel(0,200)
            # now click the buy button
            buy = page.locator(selector='button.ncss-btn-primary-dark')
            print(buy.inner_html())
            buy.click()
        except IndexError:
            pass
    else:
        pass

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    buy_product(playwright)
