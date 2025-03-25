import os

from models import *
from controllers import *
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
    'By programming languages',
    'Back'
]

# Load data
tester_manager = TesterManager()
developer_manager = DevManager()

def main():
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

                any_key = input("Press any key to back to the main menu")
                if any_key:
                    continue

            case 2:
                os.system('cls')
                # Add Employee (Developer or Tester)
                emp_name = input("Enter employee name: ")
                try:
                    base_sal = int(input("Enter base salary: "))
                except ValueError:
                    print("Invalid salary input! Please enter a number.")
                    continue
                emp_type = input("Add Developer (d) or Tester (t): ").lower()

                if emp_type == 'd':
                    team_name = input("Enter team name: ")
                    programming_languages = input("Enter programming languages (comma-separated): ").lower().split(',')
                    try:
                        exp_year = int(input("Enter experience years: "))
                    except ValueError:
                        print("Invalid experience years input! Please enter a number.")
                        continue
                    is_leader = False
                    
                    if not developer_manager.has_leader(team_name.lower()):
                        is_leader = input("Is this developer a leader? (y/n): ").lower() == 'y'

                    if is_leader:
                        try:
                            bonus_rate = float(input("Enter bonus rate (e.g., 0.1 for 10%): "))
                        except ValueError:
                            print("Invalid bonus rate input! Please enter a number.")
                            continue
                        new_dev = TeamLeader(emp_name, base_sal, team_name, programming_languages, exp_year, bonus_rate)
                    else:
                        new_dev = Developer(emp_name, base_sal, team_name, programming_languages, exp_year)

                    if developer_manager.add_dev(new_dev):
                        print(f"Success: Added developer '{emp_name}' to team '{team_name}'.")
                    else:
                        print("Error: Failed to add developer. Check for duplicate ID or team leader conflict.")
                
                elif emp_type == 't':
                    test_type = input("Enter tester type (AM/MT): ").upper()
                    try:
                        tester_type = TesterType[test_type]  
                    except KeyError:
                        print("Invalid tester type! Choose one of AM, MT.")
                        continue

                    try:
                        bonus_rate = float(input("Enter bonus rate (e.g., 0.1 for 10%): "))
                    except ValueError:
                        print("Invalid bonus rate input! Please enter a number.")
                        continue
                    emp_id = id_generator() 
                    new_tester = Tester(emp_name, base_sal, bonus_rate, tester_type, emp_id)

                    if tester_manager.add_tester(new_tester):
                        print(f"Success: Added tester '{emp_name}' of type '{tester_type.name}'.")
                    else:
                        print("Error: Failed to add tester. Check for duplicate ID.")
                else:
                    print("Invalid employee type!")

                any_key = input("Press any key to back to the main menu")
                if any_key:
                    continue
                
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
                        base_sal = input("Enter new base salary (leave blank to keep current): ")
                        if base_sal:
                            emp.set_base_salary(int(base_sal))
                    except ValueError:
                        print("Invalid input for base salary. Keeping current value.")

                    # Check if the employee is a Developer or TeamLeader
                    if isinstance(emp, Developer):
                        print(f"Current Programming Languages: {', '.join(emp.get_languages())}")
                        programming_languages = input("Enter new programming languages (comma-separated, leave blank to keep current): ").lower()
                        if programming_languages:
                            emp.set_languages(programming_languages.split(','))

                        print(f"Current Experience Years: {emp.get_exp_year()}")
                        try:
                            exp_year = input("Enter new experience years (leave blank to keep current): ")
                            if exp_year:
                                emp.set_exp_year(int(exp_year))
                        except ValueError:
                            print("Invalid input for experience years. Keeping current value.")

                        # Check if the developer is a TeamLeader
                        if isinstance(emp, TeamLeader):
                            print(f"Current Bonus Rate: {emp.get_bonus_rate()}")
                            try:
                                bonus_rate = input("Enter new bonus rate (leave blank to keep current): ")
                                if bonus_rate:
                                    emp.set_bonus_rate(float(bonus_rate))
                            except ValueError:
                                print("Invalid input for bonus rate. Keeping current value.")
                        
                        if not emp.is_leader():
                            update_leader = input(f"Do you want to update {emp.get_name()} as a Team Leader ? (y/n): ").lower() == 'y'
                            if update_leader:
                                developer_manager.update_leader(emp)
                                
                    # Check if the employee is a Tester
                    elif isinstance(emp, Tester):
                        print(f"Current Tester Type: {emp.get_type().name}")
                        tester_type = input("Enter new tester type (AM/MT, leave blank to keep current): ").upper()
                        if tester_type:
                            try:
                                emp.set_type(TesterType[tester_type])
                            except KeyError:
                                print("Invalid tester type. Keeping current value.")

                        print(f"Current Bonus Rate: {emp.get_bonus_rate()}")
                        try:
                            bonus_rate = input("Enter new bonus rate (leave blank to keep current): ")
                            if bonus_rate:
                                emp.set_bonus_rate(float(bonus_rate))
                        except ValueError:
                            print("Invalid input for bonus rate. Keeping current value.")

                    print("Employee updated successfully!")
                    developer_manager.save_dev()
                    tester_manager.save_testers()
                else:
                    print("Error: Employee not found!")
                    
                any_key = input("Press any key to back to the main menu")
                if any_key:
                    continue
                
            case 4:
                # Search Employee
                while True:
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
                                
                            any_key = input("Press any key to back to go back.")
                            if any_key:
                                continue
                        case 2:
                            # Find tester with the highest salary
                            highest_salary = tester_manager.get_max_salary()
                            top_tester = tester_manager.get_highest_salary_testers()
                            if top_tester:
                                print(f"Testers with the highest salary with {highest_salary}:")
                                for tester in top_tester:
                                    print(tester)
                            else:
                                print("No testers found.")
                            
                            any_key = input("Press any key to back to go back.")
                            if any_key:
                                continue

                        case 3:
                            languages = input("Enter programming languages (comma-separated): ").split(',')
                            results = developer_manager.search_dev_by_programming_languages(languages)
                            if results:
                                print(f"Found {len(results)} developer(s) proficient in {', '.join(languages)}:")
                                for dev in results:
                                    print(f"- {dev}")
                            else:
                                print("No developers found with those programming languages.")
                                
                            any_key = input("Press any key to back to go back.")
                            if any_key:
                                continue
                        
                        case 4:
                            break

            case 5:
                # Store data to file
                if developer_manager.save_dev() and tester_manager.save_testers():
                    print("Data stored successfully!")
                else:
                    print("Error storing data!")

                any_key = input("Press any key to back to the main menu")
                if any_key:
                    continue
                
            case 6:
                # Sort Employee
                sort_choice = input("Sort by Name (n) or Salary (s): ").lower()
                if sort_choice == 'n':
                    developer_manager.sort_by("name")
                    tester_manager.sort_by("name")
                    print("Employees sorted by name.")
                elif sort_choice == 's':
                    developer_manager.sort_by("salary", reverse=True)
                    tester_manager.sort_by("salary", reverse=True)
                    print("Employees sorted by salary.")
                else:
                    print("Invalid sort option!")

                any_key = input("Press any key to back to the main menu")
                if any_key:
                    continue
                
            case 7:
                # Exit
                print("Exiting the Developer Management System. Goodbye!")
                break

            case _:
                print("Invalid choice. Please try again.")


if __name__ == '__main__':
    main()