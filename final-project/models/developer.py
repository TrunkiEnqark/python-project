from models.employee import Employee
from utils.utils import id_generator

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
    
    def get_exp_year(self) -> int:
        return self.__exp_year
    
    def is_leader(self) -> bool:
        return self.__is_leader
    
    def get_salary(self) -> int:
        if self.__exp_year >= 5:
            return self.get_base_salary() + self.__exp_year * 2000000
        elif self.__exp_year >= 3:
            return self.get_base_salary() + self.__exp_year * 1000000
        return self.get_base_salary()
    
    def get_team_name(self) -> str:
        return self.__team_name
    
    def to_dict(self) -> dict:
        return {
            'emp_id': self.get_id(),
            'emp_name': self.get_name(),
            'base_sal': self.get_base_salary(),
            'team_name': self.__team_name,
            'programming_languages': ','.join(self.__programming_languages),
            'exp_year': self.__exp_year,
            'salary': self.get_salary(),
            'is_leader': self.__is_leader
        }
        
    def set_languages(self, new_languages: list[str]):
        self.__programming_languages = new_languages

    def set_exp_year(self, new_exp_year: int):
        self.__exp_year = new_exp_year

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

    def set_bonus_rate(self, new_bonus_rate: float):
        self.__bonus_rate = new_bonus_rate
    
    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict['bonus_rate'] = self.__bonus_rate
        return base_dict