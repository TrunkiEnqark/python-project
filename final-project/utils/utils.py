import uuid

def id_generator() -> str:
    return hex(uuid.uuid4().fields[0])[2:]

def menu(options: list[str], attempts: int = 3) -> int:
    for (idx, option) in enumerate(options):
        print(f"{idx + 1}. {option}")
    while attempts > 0:
        try:
            option = int(input(f"Choose your option, enter a number from 1 - {len(options)}: "))
            if 1 <= option and option <= len(options):
                break
            print(f"The number needs to be in the range between 1 and {len(options)}!")
        except ValueError:
            print("Please choose a valid number!")
        attempts -= 1
    return option # return the user's option