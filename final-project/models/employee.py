from abc import ABC, abstractmethod
from ..utils.utils import id_generator

class Employee(ABC):
    # Constructor
    # emp_code will be generating by id_generator using uuid
    def __init__(self, emp_name: str, base_sal: int):
        self.__emp_id = id_generator()
        self.__emp_name = emp_name
        self._base_sal = base_sal
    
    def __str__(self):
        return f'{self.__emp_id}_{self.__emp_name}_{str(self._base_sal)}'
    
    @abstractmethod
    def get_salary(self):
        pass