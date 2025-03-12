import os

from models import *
from utils.utils import *

OPTIONS = [
    'Show the Employee list',
    'Add Employee',
    'Update Employee',
    'Search Employee',
    'Store data to file',
    'Sort Employee',
    'Exit'
]

SEARCH_MENU = [
    'By name',
    'By salary (Tester with highest salary)',
    'By programming languages'
]

# Load data
tester_manager = TesterManager()
developer_manager = DevManager()

if __name__ == '__main__':
    while True:
        os.system('cls')
        print("\n=== Developer Management System ===")
        choice = menu(OPTIONS)
        match choice:
            case 1:
                # Show employees
                os.system('cls')
                print('\n=== Employee List ===')
                print('Developer Table:')
                developer_manager.display_all()
                print('Tester Table:')
                tester_manager.display_all()

                back = input('Press "b" to go back: ').lower()
                if back == 'b':
                    continue

            case 2:
                os.system('cls')
                # Add Employee (Developer or Tester)
                emp_name = input("Enter employee name: ")
                base_sal = int(input("Enter base salary: "))
                emp_type = input("Add Developer (d) or Tester (t): ").lower()

                if emp_type == 'd':
                    team_name = input("Enter team name: ")
                    programming_languages = input("Enter programming languages (comma-separated): ").split(',')
                    exp_year = int(input("Enter experience years: "))
                    is_leader = False
                    
                    if developer_manager.has_leader(team_name):
                        is_leader = input("Is this developer a leader? (y/n): ").lower() == 'y'

                    if is_leader:
                        bonus_rate = float(input("Enter bonus rate (e.g., 0.1 for 10%): "))
                        new_dev = TeamLeader(emp_name, base_sal, team_name, programming_languages, exp_year, bonus_rate)
                    else:
                        new_dev = Developer(emp_name, base_sal, team_name, programming_languages, exp_year)

                    if developer_manager.add_dev(new_dev):
                        print(f"Success: Added developer '{emp_name}' to team '{team_name}'.")
                    else:
                        print("Error: Failed to add developer. Check for duplicate ID or team leader conflict.")
                
                elif emp_type == 't':
                    test_type = input("Enter tester type (AT/AM/MT): ").upper()
                    try:
                        tester_type = TesterType[test_type]  
                    except KeyError:
                        print("Invalid tester type! Choose one of AT, AM, MT.")
                        continue

                    bonus_rate = float(input("Enter bonus rate (e.g., 0.1 for 10%): "))
                    emp_id = id_generator() 
                    new_tester = Tester(emp_name, base_sal, bonus_rate, tester_type, emp_id)

                    if tester_manager.add_tester(new_tester):
                        print(f"Success: Added tester '{emp_name}' of type '{tester_type.name}'.")
                    else:
                        print("Error: Failed to add tester. Check for duplicate ID.")
                else:
                    print("Invalid employee type!")

            case 3:
                os.system('cls')
                # Update Employee
                emp_id = input("Enter employee ID to update: ")
                emp = developer_manager.get_dev(emp_id) or tester_manager.get_tester(emp_id)

                if emp:
                    print(f"Current Name: {emp.get_name()}")
                    emp_name = input("Enter new name (leave blank to keep current): ")
                    if emp_name:
                        emp.set_name(emp_name)

                    print(f"Current Base Salary: {emp.get_base_salary()}")
                    try:
                        base_sal = int(input("Enter new base salary (leave blank to keep current): "))
                        emp.set_base_salary(base_sal)
                    except ValueError:
                        pass

                    if isinstance(emp, Developer):
                        print(f"Current Programming Languages: {', '.join(emp.get_languages())}")
                        programming_languages = input("Enter new programming languages (comma-separated, leave blank to keep current): ")
                        if programming_languages:
                            emp.set_languages(programming_languages.split(','))
                    
                    print("Employee updated successfully!")
                    developer_manager.save_dev()
                    tester_manager.save_tester()
                else:
                    print("Error: Employee not found!")

            case 4:
                # Search Employee
                os.system('cls')
                print("\n=== Search Employee ===")
                search_choice = menu(SEARCH_MENU)

                match search_choice:
                    case 1:
                        name = input("Enter employee name: ")
                        results = developer_manager.search_dev_by_name(name) + tester_manager.search_tester_by_name(name)
                        if results:
                            print(f"Found {len(results)} employee(s):")
                            for emp in results:
                                print(f"- {emp}")
                        else:
                            print("No employees found with that name.")

                    case 2:
                        # Find tester with the highest salary
                        top_tester = tester_manager.get_highest_salary_tester()
                        if top_tester:
                            print(f"Tester with the highest salary: {top_tester.get_name()} with salary {top_tester.get_salary()}")
                        else:
                            print("No testers found.")

                    case 3:
                        languages = input("Enter programming languages (comma-separated): ").split(',')
                        results = developer_manager.search_dev_by_programming_languages(languages)
                        if results:
                            print(f"Found {len(results)} developer(s) proficient in {', '.join(languages)}:")
                            for dev in results:
                                print(f"- {dev}")
                        else:
                            print("No developers found with those programming languages.")

            case 5:
                # Store data to file
                if developer_manager.save_dev() and tester_manager.save_tester():
                    print("Data stored successfully!")
                else:
                    print("Error storing data!")

            case 6:
                # Sort Employee
                sort_choice = input("Sort by Name (n) or Salary (s): ").lower()
                if sort_choice == 'n':
                    developer_manager.sort_by_name()
                    tester_manager.sort_by_name()
                    print("Employees sorted by name.")
                elif sort_choice == 's':
                    developer_manager.sort_by_salary()
                    tester_manager.sort_by_salary()
                    print("Employees sorted by salary.")
                else:
                    print("Invalid sort option!")

            case 7:
                # Exit
                print("Exiting the Developer Management System. Goodbye!")
                break

            case _:
                print("Invalid choice. Please try again.")
