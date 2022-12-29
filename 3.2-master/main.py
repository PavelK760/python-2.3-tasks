import csv
import os
import time

from multiprocessing import Pool
from line_profiler import LineProfiler

profiler = LineProfiler()

def get_filenames_from_dir(dir_name: str) -> list[str]:
	return list(map(lambda x: f"./{dir_name}/" + x, list(os.walk(f".//{dir_name}"))[0][2]))


class DataParser:
	@staticmethod
	def parse_sliced_year(date: str) -> int:
		return int(date[:4])
	
	# @staticmethod
	# def strptime_parse_year(date: str) -> int:
	# 	return datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').year
	#
	# @staticmethod
	# def dateutil_parse_year(date: str) -> int:
	# 	return parse(date).year


class Vacancy:
	"""
	Класс для представления вакансии.

	Attribytes:
		vacancy ({}): Словарь с данными о вакансии
	"""
	currency_rate = {
		"AZN": 35.68, "BYR": 23.91, "EUR": 59.90, "GEL": 21.74, "KGS": 0.76,
		"KZT": 0.13, "RUR": 1, "UAH": 1.64, "USD": 60.66, "UZS": 0.0055,
	}
	
	def __init__(self, vacancy):
		"""
		Инициализирует объект Vacancy, выполняет конвертацию для целочисленных полей

		Args:
			vacancy ({}): словарь с данными

		:returns None
		"""
		self.name = vacancy['name']
		self.salary_from = int(float(vacancy['salary_from']))
		self.salary_to = int(float(vacancy['salary_to']))
		self.salary_currency = vacancy['salary_currency']
		self.salary_average = self.currency_rate[self.salary_currency] * (self.salary_from + self.salary_to) / 2
		self.area_name = vacancy['area_name']
		self.year = DataParser.parse_sliced_year(vacancy['published_at'])


class DataSet:
	"""
		Отвечает за чтение и подготовку данных из CSV-файла (универсальный парсер CSV)
	"""
	
	def __init__(self, file_name, vacancy_name):
		"""
		Инициализирует объект Vacancy, выполняет конвертацию для целочисленных полей

		Args:
			file_name (str) название файла
			vacancy_name (str) название вакансии

		:returns None
		"""
		self.file_name = file_name
		self.vacancy_name = vacancy_name
	
	@staticmethod
	def increment_dict(dictionary, key, amount):
		"""Увеличивает словарь на определённое количество
		# >>> DataSet.increment_dict({'a': 1, 'b': 2, 'c': 3}, 'a', 6){{'a': 7, 'b': 2, 'c': 3}}
		# >>> DataSet.increment_dict({'a': 1, 'b': 2, 'c': 3}, 'b', 6){{'a': 1, 'b': 8, 'c': 3}}
		# >>> DataSet.increment_dict({'a': 1, 'b': 2, 'c': 3}, 'c', 6){{'a': 1, 'b': 2, 'c': 9}}
		"""
		if key in dictionary:
			dictionary[key] += amount
		else:
			dictionary[key] = amount
	
	@staticmethod
	def get_average(dictionary):
		"""Находит среднее значение элементов словаря

		:returns dict

		# >>> DataSet.get_average({1: [2, 5], 2: [3, 6]}){1: 3, 2: 4}
		# >>> DataSet.get_average({1: [3, 3], 2: [4, 10]}){1: 3, 2: 7}
		# >>> DataSet.get_average({1: [2, 3], 2: [0, 16]}){1: 2, 2: 8}
		"""
		new_dictionary = {}
		for key, values in dictionary.items():
			new_dictionary[key] = int(sum(values) / len(values))
		return new_dictionary
	
	def csv_reader(self):
		"""Читает csv файл

		:returns None
		"""
		with open(self.file_name, mode='r', encoding='utf-8-sig') as file:
			reader = csv.reader(file)
			header = next(reader)
			header_length = len(header)
			for row in reader:
				if '' not in row and len(row) == header_length:
					yield dict(zip(header, row))
	
	def get_data(self):
		"""Получает данные о вакансиях на освновании полей созданного объекта

		:returns (data1, vacancies_number, data2, vacancies_number_by_name, data3, data5): Статистика по зп, статистика по
				числу вакансий, статистика вакансий по ЗП, статистика вакансий по названию, статистика вакансий по городам
		"""
		salary = {}
		salary_of_vacancy_name = {}
		salary_city = {}
		count_of_vacancies = 0
		
		for vacancy_dictionary in self.csv_reader():
			vacancy = Vacancy(vacancy_dictionary)
			self.increment_dict(salary, vacancy.year, [vacancy.salary_average])
			if vacancy.name.find(self.vacancy_name) != -1:
				self.increment_dict(salary_of_vacancy_name, vacancy.year, [vacancy.salary_average])
			self.increment_dict(salary_city, vacancy.area_name, [vacancy.salary_average])
			count_of_vacancies += 1
		
		vacancies_number = dict([(key, len(value)) for key, value in salary.items()])
		vacancies_number_by_name = dict([(key, len(value)) for key, value in salary_of_vacancy_name.items()])
		
		if not salary_of_vacancy_name:
			salary_of_vacancy_name = dict([(key, [0]) for key, value in salary.items()])
			vacancies_number_by_name = dict([(key, 0) for key, value in vacancies_number.items()])
		
		data1 = self.get_average(salary)
		data2 = self.get_average(salary_of_vacancy_name)
		data3 = self.get_average(salary_city)
		
		data4 = {}
		for year, salaries in salary_city.items():
			data4[year] = round(len(salaries) / count_of_vacancies, 4)
		data4 = list(filter(lambda a: a[-1] >= 0.01, [(key, value) for key, value in data4.items()]))
		data4.sort(key=lambda a: a[-1], reverse=True)
		data5 = data4.copy()
		data4 = dict(data4)
		data3 = list(filter(lambda a: a[0] in list(data4.keys()), [(key, value) for key, value in data3.items()]))
		data3.sort(key=lambda a: a[-1], reverse=True)
		data3 = dict(data3[:10])
		data5 = dict(data5[:10])
		
		return data1, vacancies_number, data2, vacancies_number_by_name, data3, data5
	
	@staticmethod
	def print_data(data1, data2, data3, data4, data5, data6):
		"""Печатает данные в консоль

		:returns None
		"""
		print('Динамика уровня зарплат по годам: {0}'.format(data1))
		print('Динамика количества вакансий по годам: {0}'.format(data2))
		print('Динамика уровня зарплат по годам для выбранной профессии: {0}'.format(data3))
		print('Динамика количества вакансий по годам для выбранной профессии: {0}'.format(data4))
		print('Уровень зарплат по городам (в порядке убывания): {0}'.format(data5))
		print('Доля вакансий по городам (в порядке убывания): {0}'.format(data6))


class InputConnect:
	"""отвечает за обработку параметров вводимых пользователем:
	фильтры, сортировка, диапазон вывода, требуемые столбцы, а также за печать таблицы на экран
	"""
	
	def __init__(self):
		"""Создаёт необходимые файлы и печатает на экран в зависимости от пользовательского ввода

		:returns None
		"""
		self.folder = input('Введите название папки с чанками: ')
		self.vacancy_name = input('Введите название профессии: ')
	
	def process_input(self) -> None:
		"""
		Обрабатывает входные данные, создает процессы и печатает результат
		:return: None
		"""
		files = get_filenames_from_dir(self.folder)
		pools = []
		for file in files:
			dataset = DataSet(file, self.vacancy_name)
			p = Pool(5)
			result = p.apply_async(dataset.get_data)
			pools.append(result)
		
		multi = Multiprocessing(pools)
		result = multi.get_united_dict()
		DataSet.print_data(result[0], result[1], result[2], result[3], result[4], result[5])


class Multiprocessing:
	"""
    Работает с мультипроцессингом
    Attributes:
			pools (str): Созданные пуллы
	"""
	
	def __init__(self, pools) -> None:
		self.pools = pools
	
	def get_united_dict(self) -> set:
		"""
			Возвращает результаты выполнения всех процессов
			:return: Множество результатов
		"""
		answer = self.pools[0].get()
		for i in range(1, len(self.pools)):
			for k in range(0, 4):
				answer[k].update(self.pools[i].get()[k])
		return self.pools[0].get()


if __name__ == '__main__':
	connect = InputConnect()
	start_time = time.time()
	connect.process_input()
	print("--- %s seconds ---" % (time.time() - start_time))
