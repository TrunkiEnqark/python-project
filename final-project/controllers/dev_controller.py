import os
import json

from utils.utils import display_table
from models.developer import Developer, TeamLeader

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
                            programming_languages   = d['programming_languages'].lower().split(','),
                            exp_year                = d['exp_year'],
                            bonus_rate              = d.get('bonus_rate', 0.0)
                        )
                    else:
                        developers[d['emp_id']] = Developer(
                            emp_id                  = d['emp_id'],
                            emp_name                = d['emp_name'],
                            base_sal                = d['base_sal'],
                            team_name               = d['team_name'],
                            programming_languages   = d['programming_languages'].lower().split(','),
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
            if all(lang.lower() in dev.get_languages() for lang in languages)
        ]

    def has_leader(self, team_name: str) -> bool:
        return any(dev for dev in self.developers.values() 
                   if dev.get_team_name().lower() == team_name and dev.is_leader())
    
    def find_leader(self, team_name: str) -> TeamLeader | None:
        for dev in self.developers.values():
            if isinstance(dev, TeamLeader) and dev.get_team_name() == team_name:
                return dev
        return None
    
    def update_leader(self, dev: Developer) -> bool:
        if not isinstance(dev, Developer):
            return False
        
        team_name = dev.get_team_name()
        current_leader = self.find_leader(team_name) 

        if current_leader:
            if current_leader.get_id() == dev.get_id():
                print(f"{dev.get_name()} is already the Team Leader.")
                return False
            
            print(f"Demoting {current_leader.get_name()} to Developer.")
            self.developers[current_leader.get_id()] = Developer(
                emp_name=current_leader.get_name(),
                base_sal=current_leader.get_base_salary(),
                team_name=team_name,
                programming_languages=current_leader.get_languages(),
                exp_year=current_leader.get_exp_year(),
                emp_id=current_leader.get_id(),
                is_leader=False
            )

        print(f"Promoting {dev.get_name()} as the new Team Leader of {team_name}.")
        
        bonus_rate = float(input("Enter bonus rate: "))
        
        self.developers[dev.get_id()] = TeamLeader(
            emp_name=dev.get_name(),
            base_sal=dev.get_base_salary(),
            team_name=team_name,
            programming_languages=dev.get_languages(),
            exp_year=dev.get_exp_year(),
            bonus_rate=bonus_rate,
            emp_id=dev.get_id()
        )

        self.save_dev()
        return True

    def display_all(self):
        if not self.developers:
            return 
        data = [dev.to_dict() for dev in self.developers.values()]
        display_table(data)
        
    def sort_by(self, key: str, reverse=False): # key = "name" or "salary"
        key_map = {
            "name": lambda d: d.get_name(),
            "salary": lambda d: d.get_salary()
        }
        
        if key not in key_map:
            raise ValueError(f"Invalid sort key: {key}. Choose 'name' or 'salary'.")
        
        self.developers = {
            dev.get_id(): dev
            for dev in sorted(self.developers.values(), key=key_map[key], reverse=reverse)
        } 
        data = [dev.to_dict() for dev in self.developers.values()]
        display_table(data)