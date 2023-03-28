import argparse


def cli():


    parser = argparse.ArgumentParser(
        description='Find, delete a student, group, or course in the database or '
                    'generate random data and add it into database'
    )

    find_delete_group = parser.add_mutually_exclusive_group(required=False)
    id_name_group = parser.add_mutually_exclusive_group(required=False)

    find_delete_group.add_argument('--find', choices=['student', 'group', 'course'],
                                   help='Find an item in the database')
    find_delete_group.add_argument('--delete', choices=['student', 'group', 'course'],
                                   help='Delete an item from the database')

    id_name_group.add_argument('--name', help='Name of the item to find or delete', required=False)
    id_name_group.add_argument('--id', type=int, help='ID of the item to find or delete', required=False)

    parser.add_argument('--random', help='Generete random data and adds it to database', action='store_true',
                        required=False)
    parser.add_argument('--run', help='Run Flask API app', action='store_true', required=False)

    args = parser.parse_args()

    return args
