import json
import requests

import api


class CurrencyExchange:
    """
    A class to interact with the Exchange Rate API for fetching and calculating currency exchange rates.

    Attributes:
        token (str): API token for authentication.
        url (str): Base URL for the Exchange Rate API.
    """

    def __init__(self, token: str) -> None:
        """
        Initialize the CurrencyExchange class with the API token.

        Args:
            token (str): API token for authentication.
        """
        self.token = token
        self.url = api.API_URL

    def get_ex_rates(self, currency: str) -> dict | str:
        """
        Get the latest exchange rates for a specific currency.

        Args:
            currency (str): The ISO 4217 currency code (e.g., USD, EUR).

        Returns:
            dict | str: JSON-formatted string of conversion rates if successful,
                        otherwise an error message.
        """
        result = requests.get(f'{self.url}{self.token}/latest/{currency}')
        if result.status_code == 200:
            return json.dumps(result.json()['conversion_rates'], indent=2)

        return f"Request error with status code: {result.status_code}"

    def get_ex_rate_for_currencies(self, convert_to: str, convert_from: str) -> float | str:
        """
        Get the exchange rate for a specific currency pair.

        Args:
            convert_to (str): The target currency code.
            convert_from (str): The source currency code.

        Returns:
            float | str: The conversion rate if successful, otherwise an error message.
        """
        result = requests.get(f'{self.url}{self.token}/pair/{convert_from}/{convert_to}')
        if result.status_code == 200:
            return result.json()['conversion_rate']

        return f"Request error with status code: {result.status_code}"

    def exchange_from_to(self, convert_from: str, convert_to: str, amount: float) -> float | str:
        """
        Convert an amount from one currency to another.

        Args:
            convert_from (str): The source currency code.
            convert_to (str): The target currency code.
            amount (float): The amount to be converted.

        Returns:
            float | str: The converted amount if successful, otherwise an error message.
        """
        result = requests.get(f'{self.url}{self.token}/pair/{convert_from}/{convert_to}/{amount}')
        if result.status_code == 200:
            return result.json()['conversion_result']

        return f"Request error with status code: {result.status_code}"

    def get_ex_rates_at_specific_date(self, currency: str, year: int, month: int, day: int) -> float | str:
        """
        Get historical exchange rates for a specific currency on a specific date.

        Args:
            currency (str): The ISO 4217 currency code.
            year (int): The year of the historical date.
            month (int): The month of the historical date.
            day (int): The day of the historical date.

        Returns:
            float | str: JSON-formatted string of conversion rates if successful,
                        otherwise an error message.
        """
        result = requests.get(f'{self.url}{self.token}/history/{currency}/{year}/{month}/{day}')
        if result.status_code == 200:
            return json.dumps(result.json()['conversion_rates'], indent=2)

        return f"Request error with status code: {result.status_code}"


def main():
    """
    Main function to interact with the user
    for fetching and displaying currency exchange rates.
    """
    exchanger = CurrencyExchange(api.TOKEN_KEY)

    user_input = int(input(
        'What do you want to know? Please enter the number of your option\n'
        "1. Find out the actual exchange rate for a specific currency\n"
        "2. Find out the actual exchange rate for a currency pair\n"
        "3. Find out the amount of money when exchanging one currency for another\n"
        "4. Find out the exchange rate for specific date\n"
        "Your answer: "
    ))

    match user_input:
        case 1:
            currency = input(
                "What currency?\n"
                "We use ISO 4217 Three Letter Currency Codes - e.g. USD for US Dollars, EUR for Euro etc.\n"
                "Your answer: "
            )

            print(exchanger.get_ex_rates(currency))
        case 2:
            currency_from = input(
                "What currency rate do you want to know?\n"
                "We use ISO 4217 Three Letter Currency Codes - e.g. USD for US Dollars, EUR for Euro etc.\n"
                "Your answer: "
            )
            currency_to = input(
                "Relative to what currency?\n"
                "Your answer: "
            )

            print(exchanger.get_ex_rate_for_currencies(currency_from, currency_to))
        case 3:
            currency_from = input(
                "What currency rate do you want to know?\n"
                "We use ISO 4217 Three Letter Currency Codes - e.g. USD for US Dollars, EUR for Euro etc.\n"
                "Your answer: "
            )
            currency_to = input(
                "Relative to what currency?\n"
                "Your answer: "
            )
            amount = input(
                "What amount?\n"
                "Your answer: "
            )

            print(exchanger.exchange_from_to(currency_from, currency_to, float(amount)))
        case 4:
            currency = input(
                "What currency rate do you want to know?\n"
                "We use ISO 4217 Three Letter Currency Codes - e.g. USD for US Dollars, EUR for Euro etc.\n"
                "Your answer: "
            )
            year, month, day = input(
                "What date? Please enter your date in format YYYY-MM-DD"
            ).split('-')

            print(exchanger.get_ex_rates_at_specific_date(currency, int(year), int(month), int(day)))
        case _:
            print('Invalid input')


if __name__ == '__main__':
    main()
