import asyncio
from parsers import evzuttya, modivo, halloween, deezee


async def find_shoes():
    shoe_list = []

    task1 = asyncio.create_task(deezee.get_cards())
    task2 = asyncio.create_task(evzuttya.get_cards())
    task3 = asyncio.create_task(halloween.get_cards())
    task4 = asyncio.create_task(modivo.get_cards())

    shoe_list.extend(await task1)
    shoe_list.extend(await task2)
    shoe_list.extend(await task3)
    shoe_list.extend(await task4)

    return shoe_list
