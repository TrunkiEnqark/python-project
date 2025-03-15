import os
import json
import pandas as pd

from models.employee import Employee
from enum import Enum
from utils.utils import id_generator
from tabulate import tabulate

class TesterType(Enum):
    AM = 1  # Automation Test 
    MT = 2  # Manual Test

class Tester(Employee):
    # Constructor
    def __init__(self, emp_name: str, base_sal: int, 
                 bonus_rate: float, tester_type: TesterType, emp_id: str):
        super().__init__(emp_name, base_sal, emp_id)
        self.__bonus_rate = bonus_rate
        self.__type = tester_type

    def __str__(self) -> str:
        return f'{super().__str__()}_{self.__type.name}_{str(self.__bonus_rate)}'
    
    def get_salary(self) -> int:
        return int((1 + self.__bonus_rate) * self._base_sal)

    def get_type(self) -> TesterType:
        return self.__type
    
    def get_bonus_rate(self) -> float:
        return self.__bonus_rate
    
    def set_type(self, new_type: TesterType):
        self.__type = new_type
    
    def set_bonus_rate(self, new_bonus_rate: float):
        self.__bonus_rate = new_bonus_rate
    
    def to_dict(self) -> dict:
        return {
            'emp_id': self.get_id(),
            'emp_name': self.get_name(),
            'base_sal': self._base_sal,
            'bonus_rate': self.__bonus_rate,
            'type': self.__type.name,
        }

