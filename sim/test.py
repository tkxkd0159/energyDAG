a = {
    'todo1': {'task': 'Make Money'},
    'todo2': {'task': 'Play PS4'},
    'todo3': {'task': 'Study!'},
}

print('task' in a['todo1'])


class Student:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return f"Student({self.first_name!r}, {self.last_name!r})"



print(Student("dasd", "adasdasd"))