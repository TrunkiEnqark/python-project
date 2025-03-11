import uuid
print(hex(uuid.uuid4().fields[0])[2:])