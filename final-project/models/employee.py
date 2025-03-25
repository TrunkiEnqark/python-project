from abc import ABC, abstractmethod
from utils.utils import id_generator

# Abstract Class
class Employee(ABC):
    # Constructor
    # emp_code will be generating by id_generator using uuid
    def __init__(self, emp_name: str, base_sal: float, emp_id: str = None):
        if emp_id is None:
            emp_id = id_generator()
        self.__emp_id = emp_id
        self.__emp_name = emp_name
        self.__base_sal = base_sal
    
    def __str__(self) -> str:
        return f'{self.__emp_id}_{self.__emp_name}_{str(self.__base_sal)}'
    
    @abstractmethod
    def get_salary(self) -> float:
        pass
        
    def get_name(self) -> str:
        return self.__emp_name
    
    def get_id(self) -> str:
        return self.__emp_id

    def get_base_salary(self):
        return self.__base_sal 
    
    def set_name(self, new_name: str):
        self.__emp_name = new_name
        
    def set_base_salary(self, new_base_sal: float):
        self.__base_sal = new_base_sal