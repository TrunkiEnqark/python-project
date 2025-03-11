from employee import Employee

class Developer(Employee):
    # Constructor
    def __init__(self, emp_name: str, base_sal: int, 
                team_name: str, programming_languages: list[str], exp_year: int):
        super().__init__(emp_name, base_sal)
        self.__team_name = team_name
        self.__programming_languages = programming_languages
        self.__exp_year = exp_year
        
    def __str__(self):
        return f'{super.__str__()}_{self.__team_name}_{str(self.__exp_year)}'
    
    def get_salary(self):
        if self.__exp_year >= 5:
            return self._base_sal + self.__exp_year * 2000000
        elif self.__exp_year >= 3:
            return self._base_sal + self.__exp_year * 1000000
        return self._base_sal