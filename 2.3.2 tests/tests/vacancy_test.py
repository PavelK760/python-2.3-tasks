import unittest
from src.version.second import Vacancy


class TestVacancy(unittest.TestCase):
	def setUp(self) -> None:
		self.vacancy = Vacancy(
			{
				'name': 'Программист',
				'salary_from': 50000,
				'salary_to': 100000,
				'salary_currency': 'RUR',
				'area_name': 'Екатеринбург',
				'published_at': '2009-07-02T17:34:36+0300'
			}
		)

	def test_name(self):
		self.assertEqual(self.vacancy.name, 'Программист')

	def test_salary_from(self):
		self.assertEqual(self.vacancy.salary_from, 50000)

	def test_salary_to(self):
		self.assertEqual(self.vacancy.salary_to, 100000)

	def test_salary_currency(self):
		self.assertEqual(self.vacancy.salary_currency, 'RUR')

	def test_salary_average(self):
		self.assertEqual(self.vacancy.salary_average, 75000)

	def test_salary_average_double(self):
		self.vacancy = Vacancy(
			{
				'name': 'Программист',
				'salary_from': 49455.50,
				'salary_to': 50000, 'salary_currency': 'RUR',
				'area_name': 'Екатеринбург',
				'published_at': '2009-07-02T17:34:36+0300'
			}
		)

		self.assertEqual(self.vacancy.salary_average, 49727.50)

	def test_salary_year(self):
		self.assertEqual(self.vacancy.year, 2009)

	def tearDown(self) -> None:
		self.vacancy = Vacancy(
			{
				'name': 'Программист',
				'salary_from': 50000,
				'salary_to': 100000,
				'salary_currency': 'RUR',
				'area_name': 'Екатеринбург',
				'published_at': '2009-07-02T17:34:36+0300'
			}
		)


if __name__ == "__main__":
	unittest.main()