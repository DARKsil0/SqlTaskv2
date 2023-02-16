import random


def create_random_students():
    first_names = ['Emma', 'Noah', 'Olivia', 'Liam', 'Ava', 'William', 'Sophia', 'Mason', 'Isabella', 'Jacob', 'Mia',
                   'Ethan', 'Charlotte', 'Michael', 'Amelia', 'Benjamin', 'Emily', 'Daniel', 'Abigail', 'Matthew']
    last_names = ['Smith', 'Johnson', 'Williams', 'Jones', 'Brown', 'Garcia', 'Miller', 'Davis', 'Rodriguez',
                  'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Perez', 'Sanchez', 'Gomez', 'Moore', 'Taylor',
                  'Anderson', 'Thomas']
    students = []
    for i in range(200):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        students.append((first_name, last_name))
    return students


def create_random_group():
    groups = []
    for i in range(10):
        name = ''.join([random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for j in range(2)]) + '-' + ''.join(
            [random.choice('0123456789') for j in range(2)])
        groups.append(name)

    return groups


