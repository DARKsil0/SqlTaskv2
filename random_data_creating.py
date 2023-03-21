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


def create_random_courses():
    courses = [
        {'name': 'math', 'description': 'Learn the fundamentals of mathematics and problem-solving skills.'},
        {'name': 'biology', 'description': 'Study the science of life and explore living organisms and their interactions.'},
        {'name': 'chemistry', 'description': 'Discover the properties of matter and chemical reactions.'},
        {'name': 'physics', 'description': 'Explore the laws that govern the universe and the behavior of matter and energy.'},
        {'name': 'history', 'description': 'Study the past and learn about major events and their impact on society.'},
        {'name': 'english', 'description': 'Develop language skills and critical thinking through literature and writing.'},
        {'name': 'art', 'description': 'Express yourself through various art forms and learn about different styles and techniques.'},
        {'name': 'music', 'description': 'Learn to appreciate music and develop skills in playing an instrument or singing.'},
        {'name': 'computer science', 'description': 'Explore the field of computing and develop skills in programming and problem-solving.'},
        {'name': 'physical education', 'description': 'Develop physical fitness, skills, and knowledge through various activities and sports.'},
    ]
    return random.sample(courses, 10)



if __name__ == '__main__':
    print(create_random_courses())
