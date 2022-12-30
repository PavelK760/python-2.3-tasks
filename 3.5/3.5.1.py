import sqlite3
import pandas as pd


def create_sql(file_name: str) -> None:
	"""
	Генерирует SQL-файл из CSV-таблицы
	"""
	
	dataframe = pd.read_csv(file_name)
	connection = sqlite3.connect('valutes')
	dataframe.to_sql('valutes', connection, if_exists='replace', index=False)


create_sql('../src/utils/currencyparser/data.csv')
