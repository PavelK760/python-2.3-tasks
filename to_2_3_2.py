@staticmethod
def increment_dict(dictionary, key, amount):
    """Увеличивает словарь на определённое количество"""
    """Увеличивает словарь на определённое количество
    >>> DataSet.increment_dict({'a': 1, 'b': 2, 'c': 3}, 'a', 6){{'a': 7, 'b': 2, 'c': 3}}
    >>> DataSet.increment_dict({'a': 1, 'b': 2, 'c': 3}, 'b', 6){{'a': 1, 'b': 8, 'c': 3}}
    >>> DataSet.increment_dict({'a': 1, 'b': 2, 'c': 3}, 'c', 6){{'a': 1, 'b': 2, 'c': 9}}
    """
    if key in dictionary:
        dictionary[key] += amount
    else:
        dictionary[key] = amount


@staticmethod
def get_average(dictionary):
    """Находит среднее значение элементов словаря

    :returns dict

    >>> DataSet.get_average({1: [2, 5], 2: [3, 6]}){1: 3, 2: 4}
    >>> DataSet.get_average({1: [3, 3], 2: [4, 10]}){1: 3, 2: 7}
    >>> DataSet.get_average({1: [2, 3], 2: [0, 16]}){1: 2, 2: 8}
    """
    new_dictionary = {}
    for key, values in dictionary.items():
        new_dictionary[key] = int(sum(values) / len(values))
    return new_dictionary