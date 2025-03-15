import os
import json
from tabulate import tabulate
from models.tester import Tester, TesterType

class TesterManager:
    def __init__(self, file_name: str = 'data/testers.json'):
        self.__file_name = file_name
        self.testers = self.load_testers()
    
    def load_testers(self) -> dict:
        if os.path.exists(self.__file_name):
            with open(self.__file_name, 'r') as f:
                tester_data = json.load(f)
                return {
                    t['emp_id']: Tester(
                        emp_name=t['emp_name'],
                        base_sal=t['base_sal'],
                        bonus_rate=t['bonus_rate'],
                        tester_type=TesterType[t['type']],
                        emp_id=t['emp_id']
                    ) for t in tester_data
                }
        return {}
    
    def save_testers(self) -> bool:
        with open(self.__file_name, 'w') as f:
            json.dump([t.to_dict() for t in self.testers.values()], f, indent=4)
            return True
        return False
    
    def add_tester(self, new_tester: Tester) -> bool:
        emp_id = new_tester.get_id()
        if emp_id in self.testers:
            return False
        self.testers[emp_id] = new_tester
        self.save_testers()
        return True
    
    def remove_tester(self, emp_id: str) -> bool:
        if emp_id in self.testers:
            del self.testers[emp_id]
            self.save_testers()
            return True
        return False
    
    def get_tester(self, emp_id: str) -> Tester:
        return self.testers.get(emp_id, None)
    
    def search_tester_by_name(self, name: str) -> list[Tester]:
        return [tester for tester in self.testers.values() if tester.get_name() == name]
    
    def get_max_salary(self) -> int:
        if not self.testers:
            return -1
        return max(tester.get_salary() for tester in self.testers.values())
    
    def get_highest_salary_testers(self) -> list[Tester]:
        if not self.testers:
            return []
        
        max_salary = self.get_max_salary()
        return [tester for tester in self.testers.values() if tester.get_salary() == max_salary]
    
    def display_all(self):
        if not self.testers:
            return None
        data = [dev.to_dict() for dev in self.testers.values()]
        headers = data[0].keys()
        rows = [list(dev.values()) for dev in data]
        print(tabulate(rows, headers=headers, tablefmt="pretty", showindex=False))
        
    def sort_by_name(self, reverse=False):
        sorted_testers = sorted(self.testers.values(), key=lambda tester: tester.get_name(), reverse=reverse)
        data = [tester.to_dict() for tester in sorted_testers]
        headers = data[0].keys()
        rows = [list(dev.values()) for dev in data]
        print(tabulate(rows, headers=headers, tablefmt="pretty", showindex=False))

    def sort_by_salary(self, reverse=True):
        sorted_testers = sorted(self.testers.values(), key=lambda tester: tester.get_salary(), reverse=reverse)
        data = [tester.to_dict() for tester in sorted_testers]
        headers = data[0].keys()
        rows = [list(dev.values()) for dev in data]
        print(tabulate(rows, headers=headers, tablefmt="pretty", showindex=False))