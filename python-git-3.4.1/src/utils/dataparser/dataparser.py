import datetime

from openpyxl.utils import datetime
from dateutil.parser import parse


class DataParser:
	@staticmethod
	def parse_sliced_year(date: str) -> int:
		return int(date[:4])
	
	@staticmethod
	def strptime_parse_year(date: str) -> int:
		return datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').year
	
	@staticmethod
	def dateutil_parse_year(date: str) -> int:
		return parse(date).year
	