import requests
import pandas as pd
import xml.etree.ElementTree as ET


class CurrencyParser:
	"""
	Получает курсы валют из апи цб
	"""
	
	def __init__(self, filename: str) -> None:
		self.__filename = filename
		self.__url = f'https://www.cbr.ru/scripts/XML_daily.asp?date_req=02'
		self.convert_currencies = None
		self.dataframe = pd.read_csv(filename)
		self.__data = None
		self.min_date = self.dataframe['published_at'].min()
		self.max_date = self.dataframe['published_at'].max()
	
	def to_CSV(self, start: str, end: str) -> None:
		"""
		Создаёт CSV-файл с курсами валют
		:param start: Начало периода
		:param end: Конец периода
		:return: None
		"""
		start_year = int(start[:4])
		start_month = int(start[5:7])
		end_year = int(end[:4])
		end_month = int(end[5:7])
		
		dataframe = pd.DataFrame(columns=['date'] + self.convert_currencies)
		for year in range(start_year, end_year + 1):
			for month in range(1, 13):
				
				if (year == end_year and month > end_month) or (year == start_year and month < start_month):
					continue
				
				row = self.__get_row(str(month), str(year))
				if row is None:
					continue
				
				dataframe.loc[len(dataframe.index)] = row
		
		self.__data = dataframe
		dataframe.to_csv('data.csv')
	
	def get_currencies(self, n=5000) -> list:
		"""
		Выбирает только те валюты, которые встречаются в выборе более чем n раз
		:param n: Частотность
		:return: [str] Список валют
		"""
		result = []
		currencies = self.dataframe['salary_currency'].value_counts()
		for currency, amount in currencies.items():
			if amount > n:
				result.append(currency)
		self.convert_currencies = result
		return result
	
	def __get_row(self, month: str, year: str) -> list or None:
		"""
		Создаёт список курсов валют
		:param month: месяц
		:param year: Год
		:return: list
		"""
		try:
			valid_month = ('0' + str(month))[-2:]
			url = f'{self.__url}/{valid_month}/{year}'
			print(url)
			response = requests.get(url)
			tree = ET.fromstring(response.content)
			row = [f'{year}-{valid_month}']
			
			for currency in self.convert_currencies:
				if currency == 'RUR':
					row.append(1)
					continue
				
				found = False
				for curr in tree:
					if curr[1].text == currency:
						row.append(round(float(curr[4].text.replace(',', '.'))
														 / float(curr[2].text.replace(',', '.')), 6))
						found = True
						break
				
				if not found:
					row.append(None)
			
			return row
		except Exception as e:
			print(e)
			return None


a = CurrencyParser('../../../vacancies_dif_currencies.csv')
a.get_currencies()
a.to_CSV(a.min_date, a.max_date)
