from bs4 import BeautifulSoup
from aiogram.utils.markdown import hlink, hbold, hstrikethrough
from core.parsers.common import get_page


async def get_cards():
    url = 'https://modivo.ua/c/zhinky/vzuttya/rozmir_b:vzuttia_1:none:35/kolir:chornii/verkh:ekologichna_shkira_ekologichna_shkira_1/sezon:osin_zima/shirina_vzuttia:shiroka'
    response_list = [await get_page(link=url)]
    soup = BeautifulSoup(markup=response_list[0], features='lxml')
    card_list = soup.find('ul', class_='product-list')

    if card_list.find_next_sibling('div'):
        footer = card_list.find_next_sibling('div')
        pages = int(footer.find('div').find_all('a')[-1].text.strip())

        for page in range(2, pages + 1):
            _url = f'{url}?p={page}'
            response_list.append(await get_page(link=_url))

    card_info_list = []
    for each_page in response_list:
        src = each_page
        soup = BeautifulSoup(src, 'lxml')
        card_list = soup.find_all('li', class_='product')

        for card in card_list:
            card_link = card.find('a').get('href')
            link = f'https://modivo.ua{card_link}'

            card_price_info = card.find('a').find('div', class_='wrapper').find_all('div', recursive=False)
            current_price = card_price_info[-1].text.strip()

            card_brand = card.find('a').find('span', class_='product-card-name brand').text.strip()
            card_title = card.find('a').find('span', class_='product-card-name name').text.strip()
            card_link = hlink(card_brand, link)

            if len(card_price_info) > 1:
                base_price = card_price_info[0].find('div', class_='price-regular').text.strip()
                discount = card_price_info[0].find('div', class_='discount').text.strip()

                card_current_price = hbold(f"Ціна зі знижкою: {current_price}")
                card_base_price = "Стара ціна: " + f"{hstrikethrough(base_price)}"
                card_discount = hbold(f"Знижка: {discount}")
                card_info_list.append(
                    f"{card_link}\n{card_title}\n{card_current_price}\n{card_base_price}\n{card_discount}"
                )
            else:
                card_current_price = hbold(f"Ціна: {current_price}")
                card_info_list.append(
                    f"{card_link}\n{card_title}\n{card_current_price}"
                )
    return card_info_list


if __name__ == '__main__':
    import asyncio
    asyncio.run(get_cards())
