import os

from apis.wialon.core import CustomWialon


def get_wialon() -> CustomWialon:
    wialon = CustomWialon(token=os.getenv("TOKEN"), host=os.getenv("HOST"))
    return wialon
