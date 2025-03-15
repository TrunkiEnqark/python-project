import os
import json
from tabulate import tabulate

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
                   if dev.get_team_name() == team_name and dev.is_leader())
        
    def display_all(self):
        if not self.developers:
            return None
        data = [dev.to_dict() for dev in self.developers.values()]
        # display_table(data)
        headers = data[0].keys()
        rows = [list(dev.values()) for dev in data]
        print(tabulate(rows, headers=headers, tablefmt="pretty", showindex=False))
        
    def sort_by_name(self, reverse=False):
        sorted_devs = sorted(self.developers.values(), key=lambda dev: dev.get_name(), reverse=reverse)
        data = [dev.to_dict() for dev in sorted_devs]
        headers = data[0].keys()
        rows = [list(dev.values()) for dev in data]
        print(tabulate(rows, headers=headers, tablefmt="pretty", showindex=False))

    def sort_by_salary(self, reverse=True):
        sorted_devs = sorted(self.developers.values(), key=lambda dev: dev.get_salary(), reverse=reverse)
        data = [dev.to_dict() for dev in sorted_devs]
        headers = data[0].keys()
        rows = [list(dev.values()) for dev in data]
        print(tabulate(rows, headers=headers, tablefmt="pretty", showindex=False))
