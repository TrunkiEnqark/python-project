from developer import Developer

class TeamLeader(Developer):
    # Contructor 
    def __init__(self, emp_name: str, base_sal: int, 
                team_name: str, programming_languages: list[str], exp_year: int,
                bonus_rate: int):
        super().__init__(emp_name, base_sal, team_name, programming_languages, exp_year)
        self.__bonus_rate = bonus_rate
    
    def get_salary(self):
        return (1 + self.__bonus_rate) * super().get_salary()