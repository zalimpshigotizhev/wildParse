from services.base import Service
import asyncio


class Wildberries(Service):
    def __init__(self):
        self.BASE_URL = "https://card.wb.ru"

    async def get_detail_product_by_artikul(self, artikul: int) -> dict:
        url = f"{self.BASE_URL}/cards/v1/detail"
        params = {
            "appType": 1,
            "curr": "rub",
            "dest": -1257786,
            "spp": 30,
            "nm": artikul
        }
        data = await self.fetch_json(url=url, **params)

        results = data.get("data").get("products")

        if not results:
            return {"error": "Такого артикула не существует!"}
        return results[0]

