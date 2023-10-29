import json

from typing import Any

OP_CAST = {'eq': '=', 'gte': '>', 'lte': '<'}


def parse_data_json(file_name: str) -> tuple[list[float], list[float], list[Any]]:
    data = json.load(open(file_name))
    c = data['f']
    b = [constraint['b'] for constraint in data['constraints']]

    a = [constraint['coefs'] + list(OP_CAST[constraint['type']])
         for constraint in data['constraints']]
    return a, b, c

