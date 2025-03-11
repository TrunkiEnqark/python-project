from models.employee import Employee
from enum import Enum

class TesterType(Enum):
    AT = 1 # Automation Test
    AM = 2 # AM/Manual Test
    MT = 3 # MT

class Tester(Employee):
    # Constructor
    def __init__(self, emp_name: str, base_sal: int,
                 bonus_rate: int, type: TesterType):
        super().__init__(emp_name, base_sal)
        self.__bonus_rate = bonus_rate
        self.type = type
    
    def get_salary(self) -> int:
        return (1 + self.__bonus_rate) * self._base_sal