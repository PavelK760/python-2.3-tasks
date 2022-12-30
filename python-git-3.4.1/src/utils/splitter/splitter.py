import csv
from src.utils.dataparser.dataparser import DataParser
import pandas as pd


class ParserData:
	"""
		Класс для представления данных в удобном формате для CSV Splitter'a
    Attributes:
      fields (list[str]): Заголовки CSV-файлов
      data: (dict[int, list]): Данные CSV-файлов по годам
	"""
	
	def __init__(self, fields: list[str], data: dict[int, list]):
		self.fields = fields
		self.data = data


class Parser:
	"""
		Класс для разделения файла с вакансиями по годам
		Attributes:
			file_name (str): Название файла(путь) относительно расположения скрипта
  """
	
	def __init__(self, file_name: str):
		self.__file_name = file_name
	
	def create_data(self) -> ParserData:
		"""
    	Создаёт данные для сплиттера
    	:returns: CSVSplitterData
    """
		data = {}
		with open(self.__file_name, mode='r', encoding='utf-8-sig') as f:
			reader = csv.reader(f)
			titles = next(reader)
			titles_count = len(titles)
			for row in reader:
				if '' not in row and len(row) == titles_count:
					row_year = DataParser.parse_sliced_year(row[-1])
					if row_year not in data.keys():
						data[row_year] = [row]
					else:
						data[row_year].append(row)
		
		return ParserData(titles, data)
	
	def create_files(self, data: ParserData) -> None:
		"""
			Создаёт новые файлы из исходного
			:param data: Данные
			:returns: None
		"""
		for key in data.data.keys():
			df = pd.DataFrame(data.data[key], columns=data.fields)
			df.to_csv(f'../../data/{key}.csv', index=False)
			
	def invoke(self):
		"""
		Запускат сплиттер
		:return: None
		"""
		self.create_files(self.create_data())


parser = Parser('../../../vacancies_by_year.csv')
parser.invoke()
