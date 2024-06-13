"""
the network enumerations
"""
from enum import Enum


class Network(str, Enum):
    """
    The network enumerations
    """
    MAIN = "https://notify.eskiz.uz"

    def __str__(self):
        return self.value
