import pandas as pd


class SalaryParser:
	def __init__(self, file_name: str) -> None:
		self.__currencies = pd.read_csv('../currency.csv')
		self.__available = list(self.__currencies.keys()[2:])
		self.__filename = file_name
		
	def process_salaries(self) -> None:
		"""
		Форматирует CSV файл
		:return: None
		"""
		salaries = []
		remove = []
		dataframe = pd.read_csv(self.__filename)
		
		for vacancy in dataframe.itertuples():
			s_from = str(vacancy[2])
			s_to = str(vacancy[3])
			
			if s_from != 'nan' and s_to != 'nan':
				salary = float(s_from) + float(s_to)
			elif s_from != 'nan' and s_to == 'nan':
				salary = float(s_from)
			elif s_from == 'nan' and s_to != 'nan':
				salary = float(s_to)
			else:
				remove.append(int(vacancy[0]))
				continue
				
			if vacancy[4] == 'nan' or vacancy[4] not in self.__available:
				remove.append(int(vacancy[0]))
				continue
				
			if vacancy[4] != 'RUR':
				date = vacancy[6][:7]
				coefficient = self.__currencies[self.__currencies['date'] == date][vacancy[4]].iat[0]
				salary *= coefficient
				
			salaries.append(salary)
			
		dataframe.drop(labels=remove, axis=0, inplace=True)
		dataframe.drop(labels=['salary_to', 'salary_from', 'salary_currency'], axis=1, inplace=True)
		dataframe['salary'] = salaries
		dataframe.head(100).to_csv('100.csv')


SalaryParser('../vacancies_dif_currencies.csv').process_salaries()
