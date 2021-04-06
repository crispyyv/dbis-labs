import csv


def generate_insert_statement(field_names):
    query = f"INSERT INTO main({','.join(field_names)}, year) " \
            f"VALUES " \
            f"({','.join([f'%({field})s' for field in field_names])}, %(year)s)" \
            f"ON CONFLICT DO NOTHING "
    return query


def process(row):
    for key in row:
        row[key] = row[key].replace(',', '.')
        if row[key] == 'null':
            row[key] = None


def answer_question(file_obj, cursor):
    query_2020 = """
    SELECT MAX(PHYSBALL100) FROM main WHERE YEAR=2020 AND lower(UkrTestStatus)='зараховано'
    """
    query_2019 = """
    SELECT MAX(PHYSBALL100) FROM main WHERE YEAR=2019 AND lower(UkrTestStatus)='зараховано'
    """
    cursor.execute(query_2019)
    max_ball_2019 = cursor.fetchone()[0]
    cursor.execute(query_2020)
    max_ball_2020 = cursor.fetchone()[0]
    writer = csv.DictWriter(file_obj, fieldnames=[
        'MaxBallPhysics2020',
        'MaxBallPhysics2019'
    ])
    writer.writeheader()
    writer.writerow({
        'MaxBallPhysics2020': max_ball_2020,
        'MaxBallPhysics2019': max_ball_2019
    })


def delete_metadata(cursor):
    query = """
    TRUNCATE metadata;
    """
    cursor.execute(query)


def save_state(value, type, cursor):
    if not exists_in_metadata(cursor, type):
        query = """
        INSERT INTO metadata(type, value) VALUES (%s, %s)
        """
        data = (type, value)
        cursor.execute(query, data)
    else:
        query = """
        UPDATE metadata SET value=%s WHERE type=%s
        """
        cursor.execute(query, (value, type))



def get_last_error(cursor):
    query_path = """
    SELECT value FROM metadata WHERE type='last_path'
    """
    cursor.execute(query_path)
    last_path = cursor.fetchone()
    if last_path:
        last_path = last_path[0]
    else:
        last_path = None
    query_count = """
    SELECT value FROM metadata WHERE type='last_row'
    """
    cursor.execute(query_count)
    last_row = cursor.fetchone()
    if last_row:
        last_row = int(last_row[0])
    else:
        last_row = 0
    return last_path, last_row


def exists_in_metadata(cursor, type):
    query = """
    SELECT * FROM metadata WHERE type=%s 
    """
    cursor.execute(query, (type,))
    result = cursor.fetchone()
    if result:
        return True
    return False



