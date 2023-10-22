import asyncio
import aiohttp

async def get_picture(url, session):
    async with session.get(url, allow_redirects=True) as response:
        data = await response.read()
        return data


async def main():
    url = 'https://loremflickr.com/320/240'
    async with aiohttp.ClientSession() as session:
        data = await get_picture(url, session)
        return data


if __name__ == '__main__':
    asyncio.run(main())