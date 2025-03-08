from playwright.async_api import async_playwright, TimeoutError
import asyncio


async def get_rates_from_sharaf() -> dict[str, tuple[float, float]]:
    rates = {}  # Словарь для курсов валют

    async with async_playwright() as p:
        # Запуск браузера Chromium
        browser = await p.chromium.launch(headless=True)

        # Создание новой страницы
        page = await browser.new_page()

        try:
            # Переход на сайт и ожидание загрузки элементов
            await page.goto("https://www.sharafexchange.ae/services/currency-exchange")

            # Параллельное ожидание появления элементов
            await asyncio.gather(
                page.wait_for_selector(
                    'li:has-text("USD - UNITED STATES OF AMERICA")', timeout=30000
                ),
                page.wait_for_selector(
                    'li:has-text("EUR - EUROPEAN UNION")', timeout=30000
                ),
            )

            # Извлечение курсов валют
            usd_buy, usd_sell = await get_currency_data(
                page, "USD - UNITED STATES OF AMERICA"
            )
            eur_buy, eur_sell = await get_currency_data(page, "EUR - EUROPEAN UNION")

            # Заполнение словаря курсов валют
            rates = {
                "USD": (1 / usd_buy, 1 / usd_sell),
                "EUR": (1 / eur_buy, 1 / eur_sell),
            }

        except TimeoutError:
            print("Timeout while waiting for the currency elements to appear.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            # Закрытие браузера
            await browser.close()

    return rates


async def get_currency_data(page, currency_name: str) -> tuple[float, float]:
    # Ожидание появления данных о валюте и извлечение
    locator = page.locator(f'li:has-text("{currency_name}")')

    buy = float(
        await locator.locator("div[class^='RatesDesktopView_fc_buy']").text_content()
    )
    sell = float(
        await locator.locator("div[class^='RatesDesktopView_fc_cell']").text_content()
    )

    return buy, sell
