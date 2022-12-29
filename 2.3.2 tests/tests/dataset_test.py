import unittest
from src.version.second import DataSet


class TestDataset(unittest.TestCase):
	def test_increment(self):
		subject = {'a': 1, 'b': 2, 'c': 3}

		DataSet.increment_dict(subject, 'a', 6)
		self.assertEqual(subject['a'], 7)

		DataSet.increment_dict(subject, 'd', 4)
		self.assertEqual(subject['d'], 4)

	def test_get_average(self):
		self.assertEqual(DataSet.get_average({1: [2, 5], 2: [3, 6]}), {1: 3, 2: 4})
		self.assertEqual(DataSet.get_average({1: [3, 3], 2: [4, 10]}), {1: 3, 2: 7})
		self.assertEqual(DataSet.get_average({1: [2, 3], 2: [0, 16]}), {1: 2, 2: 8})


if __name__ == "__main__":
	unittest.main()