from playwright.sync_api import sync_playwright


def get_rates_from_sharaf() -> dict[str, tuple[float, float]]:
    # Создание словаря для хранения курсов валют
    rates: dict[str, tuple[float, float]] = {"USD": (0.0, 0.0), "EUR": (0.0, 0.0)}
    browser = None  # Инициализация переменной browser

    # Запуск Playwright
    with sync_playwright() as p:
        try:
            browser = p.firefox.launch(headless=True)
            page = browser.new_page()

            # Открытие страницы
            page.goto("https://www.sharafexchange.ae/services/currency-exchange")

            # Извлечение информации о курсах
            usd_data = page.locator('li:has-text("USD - UNITED STATES OF AMERICA")')
            eur_data = page.locator('li:has-text("EUR - EUROPEAN UNION")')

            # Проверка на наличие данных на сайте
            if usd_data.count() == 0 or eur_data.count() == 0:
                raise ValueError("Не удалось найти элементы с курсами.")

            # Извлечение нужных значений для USD и EUR
            usd_buy, usd_sell = get_currency_data(usd_data)
            eur_buy, eur_sell = get_currency_data(eur_data)

            # Инвертирование курсов
            usd_to_aed_buy: float = 1 / usd_buy
            usd_to_aed_sell: float = 1 / usd_sell

            eur_to_aed_buy: float = 1 / eur_buy
            eur_to_aed_sell: float = 1 / eur_sell

            # Заполнение словаря
            rates = {
                "USD": (usd_to_aed_buy, usd_to_aed_sell),
                "EUR": (eur_to_aed_buy, eur_to_aed_sell),
            }

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            # Закрытие браузера, если он был создан
            if browser is not None:
                browser.close()

    return rates


def get_currency_data(locator):
    buy = float(
        locator.locator(".RatesDesktopView_fc_buy__62GgA").text_content().strip()
    )
    sell = float(
        locator.locator(".RatesDesktopView_fc_cell__jVUpz").text_content().strip()
    )
    return buy, sell
