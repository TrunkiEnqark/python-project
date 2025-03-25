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

def display_table(data: list[dict]):
    if not data:
        return
    
    headers = list(data[0].keys())

    col_widths = {header: max(len(header), max(len(str(item.get(header, ''))) for item in data)) for header in headers}

    separator = "+".join("-" * (col_widths[header] + 2) for header in headers)
    
    print(f"+{separator}+")
    print("| " + " | ".join(header.ljust(col_widths[header]) for header in headers) + " |")
    print(f"+{separator}+")
    
    for item in data:
        print("| " + " | ".join(str(item.get(header, '')).ljust(col_widths[header]) for header in headers) + " |")

    print(f"+{separator}+")
