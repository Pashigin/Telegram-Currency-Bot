import os

import aiohttp
from dotenv import load_dotenv

load_dotenv()
api_url = os.getenv("OFFICIAL_API_URL")
sharaf_api_url = os.getenv("SHARAF_API_URL")


# Получение курса валют из официального API
async def get_official_rate(currency_code: str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{api_url}{currency_code}") as response:
                data = await response.json()
                return data["rates"]["AED"]
    except Exception as e:
        print(f"Error getting the rate for official api {currency_code}: {e}")
        return None


# Получение курса валют из Sharaf Exchange
async def get_exchange_rates(currency_code: str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{sharaf_api_url}") as response:
                data = await response.json()
                rates = data["data"]["details"]

                for rate_data in rates:
                    if rate_data["currency_code"] == currency_code:
                        cc_buy = rate_data["fc_buy"]
                        cc_sell = rate_data["fc_sell"]
                        last_update = rate_data["last_update"]
                        return cc_buy, cc_sell, last_update
    except Exception as e:
        print(f"Error getting the rate for sharaf exchange: {e}")
        return None


# Вывод курса валют из официального API
async def check_official_currency(currency_code):
    rate = await get_official_rate(currency_code)
    if rate:
        message = (
            f"📊 <b>Официальный курс валют к AED</b>:\n\n"
            f"<i>1 {currency_code} = {rate:.4f} AED</i>"
        )
        return message
    else:
        return f"Ошибка при получении курса {currency_code} в Sharaf Exchange."


# Вывод курса валют из sharaf exchange API
async def check_currency_sharaf(currency_code):
    currency_data = await get_exchange_rates(currency_code)
    if currency_data:
        buy, sell, last_update = currency_data

        buy_rate = 1 / float(buy)
        sell_rate = 1 / float(sell)

        message = (
            f"📊 <b>Курс обменника AED/{currency_code}:</b>\n\n"
            f"Покупка:  <i>1 {currency_code} = {buy_rate:.4f} AED</i>\n"
            f"Продажа: <i>1 {currency_code} = {sell_rate:.4f} AED</i>\n\n"
            f"🕛 Обновление (UTC+4): {last_update}"
        )
        return message
    else:
        return f"Ошибка при получении курса {currency_code} в Sharaf Exchange."
