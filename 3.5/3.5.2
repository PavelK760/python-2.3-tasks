import pandas as pd
import sqlite3 as sql


dataframe = pd.read_csv('vacancies_dif_currencies.csv')
dataframe = dataframe.dropna(subset=['name', 'salary_currency', 'area_name', 'published_at'])\
	.dropna(subset=['salary_from', 'salary_to'], how='all').reset_index(drop=True)

connection = sql.connect('vacancies')
cursor = connection.cursor()


def create_vacancies_sql(row: pd.Series) -> int or None:
	if row['salary_currency'] == 'RUR':
		return round(row['salary'])
	
	cursor.execute(f"""SELECT * FROM currencies WHERE DATE = '{row['date']}'""")
	
	valutes = dict(zip([col[0] for col in cursor.description], cursor.fetchone()))
	
	if row['salary_currency'] not in valutes or valutes[row['salary_currency']] is None:
		return None
	
	return round(row['salary'] * valutes[row['salary_currency']])


dataframe['date'] = dataframe['published_at'].str[:7]
dataframe['salary'] = dataframe[['salary_from', 'salary_to']].mean(axis=1)
dataframe['salary'] = dataframe.apply(axis=1, func=create_vacancies_sql)
dataframe = dataframe[['name', 'salary', 'area_name', 'date']].dropna()
dataframe.to_sql('vacancies', con=connection, index=True, if_exists='append')
