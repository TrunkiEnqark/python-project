import os
import json
import pandas as pd

from models.employee import Employee
from utils.utils import id_generator
from tabulate import tabulate

class Developer(Employee):
    # Constructor
    def __init__(self, emp_name: str, base_sal: int, 
                team_name: str, programming_languages: list[str], exp_year: int, 
                emp_id: str = None, is_leader: bool = False):
        emp_id = emp_id or id_generator()
        super().__init__(emp_name, base_sal, emp_id)
        self.__team_name = team_name
        self.__programming_languages = programming_languages
        self.__exp_year = exp_year
        self.__is_leader = is_leader
        
    def __str__(self) -> str:
        return f'{super().__str__()}_{self.__team_name}_{str(self.__exp_year)}'
    
    def get_languages(self) -> list[str]:
        return self.__programming_languages
    
    def is_leader(self) -> bool:
        return self.__is_leader
    
    def get_salary(self) -> int:
        if self.__exp_year >= 5:
            return self._base_sal + self.__exp_year * 2000000
        elif self.__exp_year >= 3:
            return self._base_sal + self.__exp_year * 1000000
        return self._base_sal
    
    def get_team_name(self) -> str:
        return self.__team_name
    
    def to_dict(self) -> dict:
        return {
            'emp_id': self.get_id(),
            'emp_name': self.get_name(),
            'base_sal': self._base_sal,
            'team_name': self.__team_name,
            'programming_languages': ','.join(self.__programming_languages),
            'exp_year': self.__exp_year,
            'salary': self.get_salary(),
            'is_leader': self.__is_leader
        }


class TeamLeader(Developer):
    # Constructor 
    def __init__(self, emp_name: str, base_sal: int, 
                 team_name: str, programming_languages: list[str], exp_year: int, 
                 bonus_rate: float, emp_id: str = None):
        super().__init__(emp_name, base_sal, team_name, programming_languages, exp_year, emp_id, is_leader=True)
        self.__bonus_rate = bonus_rate
    
    def get_bonus_rate(self) -> float:
        return self.__bonus_rate

    def get_salary(self) -> float:
        return float((1 + self.__bonus_rate) * super().get_salary())

    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict['bonus_rate'] = self.__bonus_rate
        return base_dict


class DevManager:
    def __init__(self, file_name: str = 'data/developers.json'):
        self.__file_name = file_name
        self.developers = self.load_dev()

    def load_dev(self) -> dict:
        if os.path.exists(self.__file_name):
            with open(self.__file_name, 'r') as f:
                dev_data = json.load(f)
                developers = {}
                for d in dev_data:
                    if d.get('is_leader', False):
                        developers[d['emp_id']] = TeamLeader(
                            emp_id                  = d['emp_id'],
                            emp_name                = d['emp_name'],
                            base_sal                = d['base_sal'],
                            team_name               = d['team_name'],
                            programming_languages   = d['programming_languages'].split(','),
                            exp_year                = d['exp_year'],
                            bonus_rate              = d.get('bonus_rate', 0.0)
                        )
                    else:
                        developers[d['emp_id']] = Developer(
                            emp_id                  = d['emp_id'],
                            emp_name                = d['emp_name'],
                            base_sal                = d['base_sal'],
                            team_name               = d['team_name'],
                            programming_languages   = d['programming_languages'].split(','),
                            exp_year                = d['exp_year']
                        )
                return developers
        return {}

    def save_dev(self) -> bool:
        with open(self.__file_name, 'w') as f:
            json.dump([d.to_dict() for d in self.developers.values()], f, indent=4)
            return True
        return False

    def add_dev(self, new_dev: Developer | TeamLeader) -> bool:
        emp_id = new_dev.get_id()
        if emp_id in self.developers or (new_dev.is_leader() and self.has_leader(new_dev.get_team_name())):
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
        return self.developers.get(emp_id, None)

    def search_dev_by_name(self, name: str) -> list[Developer]:
        return [dev for dev in self.developers.values() if dev.get_name() == name]

    def search_dev_by_programming_languages(self, languages: list[str]) -> list[Developer]:
        return [
            dev for dev in self.developers.values()
            if all(lang in dev.get_languages() for lang in languages)
        ]

    def has_leader(self, team_name: str) -> bool:
        return any(dev for dev in self.developers.values() 
                   if dev.get_team_name() == team_name and dev.is_leader())
        
    def display_all(self):
        if not self.developers:
            return None
        data = [dev.to_dict() for dev in self.developers.values()]
        df = pd.DataFrame(data)
        print(tabulate(df, headers='keys', tablefmt='pretty', showindex=False))
        
    def sort_by_name(self, reverse=False):
        sorted_devs = sorted(self.developers.values(), key=lambda dev: dev.get_name(), reverse=reverse)
        data = [dev.to_dict() for dev in sorted_devs]
        df = pd.DataFrame(data)
        print(tabulate(df, headers='keys', tablefmt='pretty', showindex=False))

    def sort_by_salary(self, reverse=True):
        sorted_devs = sorted(self.developers.values(), key=lambda dev: dev.get_salary(), reverse=reverse)
        data = [dev.to_dict() for dev in sorted_devs]
        df = pd.DataFrame(data)
        print(tabulate(df, headers='keys', tablefmt='pretty', showindex=False))
