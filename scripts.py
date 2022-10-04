from playwright.sync_api import sync_playwright, Playwright, expect
from bs4 import BeautifulSoup
import pandas as pd


def run(playwright: Playwright) -> None:
    # launching the firefox browser
    browser = playwright.chromium.launch()
    
    context = browser.new_context()
    page = context.new_page()
    
    # opening the https://www.nike.com/gb/w/new-3n82y web page
    page.goto(url='https://www.nike.com/gb/w/new-3n82y')
    
    # quering the product list
    product_lists = page.query_selector_all(selector='div[data-testid="product-card__body"]')
    for i in range(len(product_lists)):
        html_page = product_lists[i].inner_html()
        soup = BeautifulSoup(html_page,'html.parser')
        status = soup.find('div',class_='product-card__messaging').text
        if status.lower() == 'Available in SNKRS'.lower():
            product_title = soup.find('div',class_='product-card__title').text
            product_price = soup.find('div',class_='product-card__price-wrapper').text
            product_link = soup.find('a',class_='product-card__link-overlay').get('href')
            data = pd.read_csv('url_links.csv')
            if data.empty:
                df = pd.DataFrame({
                    'title':[product_title],
                    'price':[product_price],
                    'url':[product_link]
                })
                df.to_csv('url_links.csv',index=False)
            else:
                df = pd.DataFrame({
                    'title':[product_title],
                    'price':[product_price],
                    'url':[product_link]
                })
                df.to_csv('url_links.csv',index=False,header=False,mode='a')
    context.close()
    browser.close()
    
    
def buy_product(playwright: Playwright,web_url) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    # Open new page
    page = context.new_page()

    # Go to https://www.nike.com/gb/launch/t/womens-air-max-97-gorge-green
    page.goto(url=web_url)
    page.mouse.wheel(0,500)
    # Click text=UK 13
    sizes = page.query_selector_all(selector='button[class="size-grid-dropdown size-grid-button"]')
    if len(sizes) != 0:
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
        except:
            pass
    else:
        pass

    # ---------------------
    context.close()
    browser.close()
    
    



with sync_playwright() as playwright:
    run(playwright)
    
data = pd.read_csv('url_links.csv')
for i in range(len(data)):
    web_url = data['url'][i]
    with sync_playwright() as playwright:
        buy_product(playwright,web_url)