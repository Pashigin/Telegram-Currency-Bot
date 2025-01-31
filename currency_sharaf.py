from playwright.sync_api import sync_playwright, TimeoutError


def get_rates_from_sharaf() -> dict[str, tuple[float, float]]:
    rates = {}  # Словарь для курсов валют

    with sync_playwright() as p:
        # Запуск браузера Chromium
        browser = p.chromium.launch(headless=True)

        # Создание новой страницы
        page = browser.new_page()

        try:
            # Переход на сайт и ожидание загрузки элементов
            page.goto("https://www.sharafexchange.ae/services/currency-exchange")

            # Ожидание появления элементов с курсами валют
            page.wait_for_selector(
                'li:has-text("USD - UNITED STATES OF AMERICA")', timeout=30000
            )
            page.wait_for_selector('li:has-text("EUR - EUROPEAN UNION")', timeout=30000)

            # Извлечение курсов валют
            usd_data = page.locator('li:has-text("USD - UNITED STATES OF AMERICA")')
            eur_data = page.locator('li:has-text("EUR - EUROPEAN UNION")')

            if usd_data.count() == 0 or eur_data.count() == 0:
                raise ValueError("Could not find currency elements.")

            usd_buy, usd_sell = get_currency_data(usd_data)
            eur_buy, eur_sell = get_currency_data(eur_data)

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
            browser.close()

    return rates


def get_currency_data(locator) -> tuple[float, float]:
    # Извлечение данных о покупке и продаже валют
    buy = float(
        locator.locator("div[class^='RatesDesktopView_fc_buy']").text_content().strip()
    )
    sell = float(
        locator.locator("div[class^='RatesDesktopView_fc_cell']").text_content().strip()
    )
    return buy, sell
