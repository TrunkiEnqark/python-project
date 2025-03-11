import uuid

def id_generator() -> str:
    return hex(uuid.uuid4().fields[0])[2:]