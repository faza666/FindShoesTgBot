from bs4 import BeautifulSoup
from aiogram.utils.markdown import hlink, hbold, hstrikethrough
from parsers.common import get_page
import math


async def get_cards():
    # url = 'https://ccc.eu/ua/zhinky/vzuttya/rozmir:35/sezon:zima'
    url = 'https://ccc.eu/ua/zhinky/vzuttya/rozmir:35/material:ekologichna_shkira/kolir:chornii/sezon:zima/uteplennya:tak'
    response_list = [await get_page(link=url)]
    soup = BeautifulSoup(markup=response_list[0], features='lxml')
    items_found_string = soup.find('span', {'class': 'c-headline_count a-typo is-text'}).text
    items_found = int(''.join(filter(str.isdigit, items_found_string)))
    items_on_page = 25
    if items_found > items_on_page:
        pages = math.ceil(items_found / items_on_page)
        for page in range(2, pages + 1):
            _url = f'{url}?page={page}'
            response_list.append(await get_page(link=_url))

    card_info_list = []
    for each_page in response_list:
        src = each_page
        soup = BeautifulSoup(src, 'lxml')
        card_list = soup \
            .find('div', {'class': 'c-grid'}) \
            .find_all('div', {'class': 'c-grid_col is-grid-col-4'})

        for card in card_list:
            card_link = card \
                .find('div', {'class': 'c-offerBox_photo', 'data-zone': 'OFFERBOX_PHOTO'}) \
                .find('a').get('href')
            link = f'https://ccc.eu{card_link}'

            card_title = card.find('a', class_='a-typo is-text').find(text=True, recursive=False)

            card_link = hlink(card_title, link)

            card_price = card \
                .find('div', class_='a-price clearfix2') \
                .find_all('span', class_='a-price_price')
            current_price = card_price[0].text.strip()

            if len(card_price) > 1:
                base_price = card_price[1].text.strip()

                discount = 100 - int(int(current_price) / (int(base_price) / 100))
                card_discount = hbold(f"Знижка: -{discount}%")
                current_price = hbold(f"Ціна зі знижкою: {current_price}")
                old_price = "Стара ціна: " + f"{hstrikethrough(base_price)}"
                card_info_list.append(
                    f"{card_link}\n{current_price}\n{old_price}\n{card_discount}"
                )
            else:
                current_price = hbold(f"Ціна: {current_price}")
                card_info_list.append(f"{card_link}\n{current_price}")

    return card_info_list


if __name__ == '__main__':
    import asyncio
    asyncio.run(get_cards())
