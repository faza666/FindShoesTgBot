from bs4 import BeautifulSoup
from aiogram.utils.markdown import hlink, hbold, hstrikethrough
import asyncio

from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By


async def set_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-blink-features=AutomationControlled')
    service = webdriver.FirefoxService(executable_path=GeckoDriverManager().install())
    driver = webdriver.Firefox(options=options, service=service)
    return driver


async def get_links():
    driver = await set_driver()
    url = 'https://deezee.eu/uk/zhinoche-vzuttya/'
    filters = '11918,35?at[2]=1202&at[12]=307952&at[109]=123453%2C123451'
    link = url + filters

    try:
        driver.get(link)
        # await asyncio.sleep(2)
        pagination_block = driver \
            .find_element(By.CLASS_NAME, 'pagination-container')

        url_list = [link]
        if len(pagination_block.find_elements(By.TAG_NAME, 'li')) > 0:
            pages = int(pagination_block.find_elements(By.TAG_NAME, 'li')[-2].text.strip())
            for page in range(2, pages + 1):
                _url = f'{url}/page:{page}{filters}'
                url_list.append(_url)

    except Exception as ex:
        print(ex)
        print('Йой! Якісь проблєми з інтернетом!...')
        return []
    return url_list


async def get_pages():
    driver = await set_driver()
    url_list = await get_links()

    if not url_list:
        return None

    item_source_list = []
    for each_link in url_list:
        try:
            driver.get(each_link)
            driver.maximize_window()
            await asyncio.sleep(2)

            item_source_list.append(driver.page_source)

        except Exception as ex:
            print(ex)

    driver.quit()
    return item_source_list


async def get_cards():
    item_source_list = await get_pages()
    item_card_list = []
    for item in item_source_list:
        soup = BeautifulSoup(item, 'lxml')

        card_holder = soup.find('div', {'data-type': 'product-list'}) \
            .find('ul')

        card_list = card_holder.find_all('div', class_='product-box gallery clearfix')

        for card in card_list:
            card_info_block = card.find('div', class_='box-left')

            card_link = card_info_block.find('h2', class_='product-name') \
                .find('a', {'data-type': 'product-url'}).get('href')
            link = f'https://deezee.eu{card_link}'

            card_title = card_info_block.find('h2', class_='product-name').text.strip()

            card_price_info = card_info_block.find('div', class_='product-price-container')
            price = card_price_info.find('span', class_='price').text.strip()
            discount_price = card_price_info.find('span', class_='discount-price').text.strip()
            base_price = card_price_info.find('span', class_='base-price').text.strip()

            card_link = hlink(f'{card_title}', link)

            if price:
                current_price = hbold(f"Ціна: {price}")
                item_card_list.append(f"{card_link}\n{current_price}")
            else:
                card_current_price = hbold(f"Ціна зі знижкою: {discount_price}")
                old_price = "Стара ціна: " + f"{hstrikethrough(base_price)}"
                discount = 100 - int(int(discount_price[:-6]) / (int(base_price[:-6]) / 100))
                card_discount = hbold(f"Знижка: -{discount}%")
                item_card_list.append(
                    f"{card_link}\n{card_current_price}\n{old_price}\n{card_discount}"
                )

    return item_card_list


if __name__ == '__main__':
    asyncio.run(get_cards())
