from bs4 import BeautifulSoup
from aiogram.utils.markdown import hlink, hbold, hstrikethrough
from parsers.common import get_page


async def get_cards():
    url = 'https://evzuttya.com.ua/c/zhinoche/grouped_size:35/kolir:chornii/uteplennia:tak/shirina_vzuttia:shiroka/verkh:ekologichna_shkira_ekologichna_shkira_1/sezon:osin_zima'
    response_list = [await get_page(link=url)]
    soup = BeautifulSoup(markup=response_list[0], features='lxml')
    card_list = soup.find('div', class_='list-container')

    if card_list.find_next_sibling('div'):
        footer = card_list.find_next_sibling('div')
        pages = int(footer.find('div', class_='pagination-items').find_all('a')[-1].text.strip())

        for page in range(2, pages + 1):
            _url = f'{url}?p={page}'
            response_list.append(await get_page(link=_url))

    item_card_list = []
    for each_page in response_list:
        soup = BeautifulSoup(each_page, 'lxml')
        card_list = soup.find_all('li', class_='product-item')

        for card in card_list:
            card_link = card.find('a').get('href')
            link = f'https://evzuttya.com.ua{card_link}'

            card_info_list = card.find('a').find_all('div', recursive=False)
            card_price_info = card_info_list[-1].find_all('div', recursive=False)
            current_price = card_price_info[0].text.strip()

            card_title_info = card_info_list[-2]
            card_brand = card_title_info.find('strong').text.strip()
            card_title = card_title_info.find('h2').text.strip()

            card_link = hlink(card_brand, link)

            if len(card_price_info) > 1:
                base_price = card_price_info[-1].text.strip()
                discount = card_info_list[-3].find('span').text.strip()

                card_current_price = hbold(f"Ціна зі знижкою: {current_price}")
                old_price = "Стара ціна: " + f"{hstrikethrough(base_price)}"
                card_discount = hbold(f"Знижка: -{discount}%")

                item_card_list.append(
                    f"{card_link}\n{card_title}\n{card_current_price}\n{old_price}\n{card_discount}"
                )
            else:
                card_current_price = hbold(f"Ціна: {current_price}")
                item_card_list.append(f"{card_link}\n{card_title}\n{card_current_price}")

    return item_card_list


if __name__ == '__main__':
    import asyncio
    asyncio.run(get_cards())
