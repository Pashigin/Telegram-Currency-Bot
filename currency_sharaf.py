import requests
import re
from bs4 import BeautifulSoup


def get_rates_from_sharaf():
    try:
        response = requests.get("https://www.sharafexchange.com/exchange-rates")
        response.raise_for_status()  # Проверка на ошибки HTTP
        soup = BeautifulSoup(response.content, "html.parser")

        # Найти строки с "US Dollar" и "Euro"
        usd_row = soup.find("td", string=re.compile("US Dollar"))
        eur_row = soup.find("td", string=re.compile("Euro"))

        # Функция для извлечения данных из строки
        def extract_rates(row):
            if row:
                columns = row.find_parent("tr").find_all("td")
                fc_buy = columns[2].text.strip() if len(columns) > 2 else None
                fc_sell = columns[3].text.strip() if len(columns) > 2 else None
                return fc_buy, fc_sell
            return None, None

        # Извлечь курсы для USD и EUR
        usd_rates = extract_rates(usd_row)
        eur_rates = extract_rates(eur_row)

        # Возвращаем кортежи с курсами
        return {"USD": usd_rates, "EUR": eur_rates}
    except Exception as e:
        return f"Ошибка: {e}"
