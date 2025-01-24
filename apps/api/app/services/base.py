import aiohttp


class Service:
    async def fetch_json(self, url: str, **kwargs):
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, params=kwargs) as response:
                # Проверка статуса ответа
                if response.status != 200:
                    raise Exception(f"Failed to fetch data: {response.status}")

                # Получение JSON-ответа
                data = await response.json()
                return data