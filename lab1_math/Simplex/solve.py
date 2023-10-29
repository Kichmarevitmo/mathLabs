import simplex as smp

from parse_data import parse_data_json


def solve_simplex(file_name: str) -> None:
    a, b, c = parse_data_json(file_name)

    new_line = '\n'
    tab = '\t'

    msg = \
    f"""
    СИМПЛЕКС-МЕТОД
    Исходные данные:
        Таблица коэффицентов и знаков:
    {new_line.join(tab + str(i) for i in a)}
        Коэфиценты целевой функции:
    {tab + str(c)}
        Ограничения:
    {tab + str(b)}
    """
    print(msg)

    # используем алгоритм симплекс-метода
    # алгоритм максимизации, поэтому flio = True
    # количество доп. переменных 0
    result = smp.my_simplex(a, b, c, flip=True, saveslack=True, counter=0)
    msg = \
    f"""
    Результат работы симлпекс-метода:
        Таблица коэффицентов:
    {new_line.join(tab + str(i) for i in result[0])}
        Значение целевой функции:
    {tab + str(result[4])}
        Значения переменных целевой функции:
    {tab + str(result[5])}
    """
    print(msg)
