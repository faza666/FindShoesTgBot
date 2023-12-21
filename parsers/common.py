import httpx


async def get_page(link):
    headers = {
        'accept-language': 'en-US,en;q=0.5',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
    }
    async with httpx.AsyncClient(headers=headers, follow_redirects=True) as htp:
        result: httpx.Response = await htp.get(url=link)
        if result.status_code != 200:
            return await get_page(link=link)
        else:
            return await result.aread()

