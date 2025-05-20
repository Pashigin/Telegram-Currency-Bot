import os
from datetime import datetime

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
                return data
    except Exception as e:
        print(f"Ошибка при получении курса с оф. API {currency_code}: {e}")
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
        print(f"Ошибка при получении курса c sharaf exchange: {e}")
        return None


async def check_official_currency(base: str, target: str = "AED") -> str:
    rates = await get_official_rate(base)

    # Проверяем, есть ли курс для base
    if not rates or "rates" not in rates:
        return f"❌ Официальный курс {base} не найден в базе"

    if target not in rates["rates"]:
        return f"❌ Официальный курс к {target} не найден в базе"

    rate = rates["rates"][target]

    dt = datetime.strptime(rates["time_last_update_utc"], "%a, %d %b %Y %H:%M:%S %z")
    last_update = dt.strftime("%d %b %Y, %H:%M")

    message = (
        f"📊 <b>Официальный курс {base} → {target}</b>:\n\n"
        f"<i>1 {base} = {rate:.4f} {target}</i>\n\n"
        f"🕛 Обновлено (UTC): {last_update}"
    )
    return message


async def check_currency_sharaf(base: str) -> str:
    currency_data = await get_exchange_rates(base)

    if currency_data:
        buy, sell, last_update = currency_data

        buy_rate = 1 / float(buy)
        sell_rate = 1 / float(sell)

        dt = datetime.strptime(last_update, "%Y-%m-%d %I:%M %p")
        last_update = dt.strftime("%d %b %Y, %H:%M")

        message = (
            f"📊 <b>Курс обменника AED → {base}:</b>\n\n"
            f"Покупка:  <i>1 {base} = {buy_rate:.4f} AED</i>\n"
            f"Продажа: <i>1 {base} = {sell_rate:.4f} AED</i>\n\n"
            f"🕛 Обновлено (UTC+4): {last_update}"
        )
        return message
    else:
        return "❌ Курса нет в базе Sharaf Exchange, либо произошла ошибка"
