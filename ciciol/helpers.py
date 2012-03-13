"""
Helpers for Ciciol
"""


def import_from_string(path):
    """
    Imports object from string path
    """
    splitted = path.split(".")
    cls = splitted[-1]
    module = __import__(".".join(splitted[:-1]), fromlist=[cls])
    return getattr(module, splitted[-1])
