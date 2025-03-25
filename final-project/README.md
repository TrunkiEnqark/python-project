# Employee Management System

## Project Structure

```
│   .gitignore
│   poetry.lock
│   pyproject.toml
│   README.md
│   requirements.txt
│
├───controllers
│       dev_controller.py
│       tester_controller.py
│       __init__.py
│
├───data
│       developers.json
│       testers.json
│
├───demo
│       demo.py
│
├───final_project
│       main.py
│       __init__.py
│
├───models
│       developer.py
│       employee.py
│       tester.py
│       __init__.py
│
├───tests
│       test.py
│       test_main.py
│       __init__.py
│
└───utils
        utils.py
        __init__.py
```

## Introduction
This is an employee management system for Developers and Testers, supporting the following functions:
- Add, update, and delete employees
- Search employees by name, salary, or programming languages
- Sort employees by salary or name
- Store and load employee data from a file
- Ensure each team has only one TeamLeader
- Implement object-oriented principles with inheritance and polymorphism

## Installation

### 1. Clone the Repository
First, clone the repository to your local machine:
```sh
git clone https://github.com/TrunkiEnqark/python-projects
cd final-project
```

### 2. Install Dependencies using Poetry
This project uses [Poetry](https://python-poetry.org/) for dependency management. If you haven't installed Poetry, install it first:
```sh
pip install poetry
```
Then, install the required dependencies:
```sh
poetry install
```

### 3. Activate the Virtual Environment
To activate the virtual environment managed by Poetry, run:
```sh
poetry shell
```

## Running the Main Program
To run the employee management system, use the command:
```sh
python final_project/main.py
```

## Running Automated Tests
The project includes a test suite located in the `test/` directory. To run all tests, use:
```sh
python test/test_main.py
```
The program will:
1. Create a sample employee list.
2. Test functions for adding, updating, deleting, searching, and sorting employees.
3. Verify salary calculations based on employee type.
4. Display test results on the screen.

Test results will be displayed in a table format with **PASS** or **FAIL** status along with execution time.