import os
import json

from models.employee import Employee
from utils.utils import id_generator

class Developer(Employee):
    # Constructor
    def __init__(self, emp_name: str, base_sal: int, 
                team_name: str, programming_languages: list[str], exp_year: int, emp_id: str):
        super().__init__(emp_name, base_sal, emp_id)
        self.__team_name = team_name
        self.__programming_languages = programming_languages
        self.__exp_year = exp_year
        
    def __str__(self) -> str:
        return f'{super().__str__()}_{self.__team_name}_{str(self.__exp_year)}'
    
    def get_languages(self) -> list[str]:
        return self.__programming_languages
    
    def get_salary(self) -> int:
        if self.__exp_year >= 5:
            return self._base_sal + self.__exp_year * 2000000
        elif self.__exp_year >= 3:
            return self._base_sal + self.__exp_year * 1000000
        return self._base_sal
    
    def to_dict(self) -> dict:
        return {
            'emp_id': self.get_id(),
            'emp_name': self.get_name(),
            'base_sal': self._base_sal,
            'team_name': self.__team_name,
            'programming_languages': ','.join(self.__programming_languages),
            'exp_year': self.__exp_year,
            'salary': self.get_salary()
        }
    
class DevManager:
    def __init__(self, file_name: str = 'data/developers.json'):
        self.__file_name = file_name
        self.developers = self.load_dev()
    
    def load_dev(self) -> dict:
        if os.path.exists(self.__file_name):
            with open(self.__file_name, 'r') as f:
                dev_data = json.load(f)
                return {d['emp_id']: Developer(emp_id=d['emp_id'],
                                               emp_name=d['emp_name'],
                                               base_sal=d['base_sal'],
                                               team_name=d['team_name'],
                                               programming_languages=d['programming_languages'].split(','),
                                               exp_year=d['exp_year']
                                            ) for d in dev_data}
        return {}
    
    def save_dev(self) -> bool:
        with open(self.__file_name, 'w') as f:
            json.dump([d.to_dict() for d in self.developers.values()], f, indent=4)
            return True
        return False
    
    def add_dev(self, new_dev: Developer) -> bool:
        emp_id = new_dev.get_id()
        if emp_id in self.developers:
            return False
        self.developers[emp_id] = new_dev
        self.save_dev()
        return True
    
    def remove_dev(self, emp_id: str) -> bool:
        if emp_id in self.developers:
            del self.developers[emp_id]
            self.save_dev()
            return True
        return False
    
    def get_dev(self, emp_id: str) -> Developer:
        if emp_id in self.developers:
            return self.developers[emp_id]
        return None
    
    def search_dev_by_name(self, name: str) -> list[Developer]:
        return [dev for dev in self.developers.values() if dev.get_name() == name]
    
    def search_dev_by_programming_languages(self, languages: list[str]) -> list[Developer]:
        devs = []
        
        for dev in self.developers.values():
            if all(lang in dev._Developer__programming_languages for lang in languages):
                devs.append(dev)
        
        return devs