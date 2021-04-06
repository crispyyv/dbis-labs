

def read_sql(path):
    with open(path) as f:
        query = f.read()
    return query


def init(cursor):
    sql = read_sql('init.sql')
    cursor.execute(sql)
