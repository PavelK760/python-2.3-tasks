import pandas as pd
from numpy import nan
from collections import namedtuple


class PandasCSVFormatter:
    def __init__(self, main_file: str, currencies_file: str):
        self.__main_file = main_file
        self.__currencies_file = currencies_file
        self.__df = pd.read_csv(main_file)

    def get_salary(self) -> list:
        """
        Конвертирует 'salary_from', 'salary_to', 'salary_currency' в salary
        """

        result = []
        currencies = pd.read_csv(self.__currencies_file)
        for row in self.__df.itertuples(index=False, name="Vacancy"):
            # print(row.salary_from)
            salary = self.get_valid_salary(row, currencies)
            # print(salary)

            result.append(salary)
        return result

    def get_valid_salary(self, row: namedtuple, currencies: pd.DataFrame) -> int or nan:
        """
        Проверяет аргументы на NaN
        Eсли данных хватает - возвращает зарплату, иначе NaN.
        """

        if pd.isna(row.salary_currency) or pd.isna(row.salary_from) and pd.isna(row.salary_to):
            return nan

        currencies = currencies.set_index('date')
        date = row.published_at[:7]

        try:
            multiplier = 1 if row.salary_currency == "RUR" else currencies[row.salary_currency][date]
        except KeyError:
            return nan

        if pd.isna(multiplier):
            return nan

        if not pd.isna(row.salary_from) and not pd.isna(row.salary_to):
            return int(multiplier * (row.salary_from + row.salary_to) // 2)
        else:
            return int(multiplier * row.salary_from) if pd.isna(row.salary_to) else int(multiplier * row.salary_to)

    def to_CSV(self, salary_values: list) -> pd.DataFrame:
        """
        Добавляет новый столбец salary
        """

        self.__df["salary_from"] = salary_values
        self.__df = self.__df.drop(columns=["salary_to", "salary_currency"])
        self.__df.rename({"salary_from": "salary"}, axis=1, inplace=True)
        return self.__df


def main() -> None:
    formatter = PandasCSVFormatter("vacancies_dif_currencies.csv", "./src/utils/currencyparser/data.csv")
    salaries = formatter.get_salary()
    df = formatter.to_CSV(salaries)
    df.to_csv("100_vac", index=False)


if __name__ == "__main__":
    main()