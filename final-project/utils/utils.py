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
        print("Không có dữ liệu để hiển thị.")
        return

    headers = set()
    for item in data:
        headers.update(item.keys())
    headers = list(headers)
    
    col_widths = {header: len(header) for header in headers}
    for item in data:
        for header in headers:
            if header in item:
                col_widths[header] = max(col_widths[header], len(str(item[header])))
    
    separator = "+" + "+".join("-" * (col_widths[header] + 2) for header in headers) + "+"
    
    print(separator)
    header_row = "| " + " | ".join(header.ljust(col_widths[header]) for header in headers) + " |"
    print(header_row)
    print(separator)
    
    for item in data:
        row_values = []
        for header in headers:
            value = str(item.get(header, "")) if header in item else ""
            row_values.append(value.ljust(col_widths[header]))
        print("| " + " | ".join(row_values) + " |")
    
    print(separator)