from api.util.singleton import Singleton

"""
Author          : Neda Peyrone
Create Date     : 05-09-2021
File            : app_config.py
Purpose         : -
"""


class AppConfig(metaclass=Singleton):

    def __init__(self, params) -> None:
        self.params = params
