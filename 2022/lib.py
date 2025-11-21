import sys
import re

def _name(prefix: str) -> str:
    ext = ("." + prefix if prefix else "" ) + ".txt"
    filename = sys.argv[0].replace(".py", ext)
    return filename

def read_lines(prefix: str = "") -> list[list[str]]:
    filename = _name(prefix)

    with open(filename, 'r') as file:
        lines = file.readlines()

    return [line.rstrip() for line in lines]

def read_content(prefix: str = "") -> list[list[str]]:
    filename = _name(prefix)

    with open(filename, 'r') as file:
        content = file.read().strip()

    return content

def ints(d: dict) -> dict:
    for k, v in d.items():
        try:
            d[k] = int(v)
        except (ValueError, TypeError):
            pass # Leave the value unchanged if it can't be converted
    return d

def min_max(gen):
    try:
        first = next(gen)
    except StopIteration:
        raise ValueError("Generator is empty")

    min_val = max_val = first
    for val in gen:
        if val < min_val:
            min_val = val
        if val > max_val:
            max_val = val
    return min_val, max_val
