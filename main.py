import time
import csv
import traceback
from dotenv import dotenv_values
from database import get_connection

from init import init
from service import generate_insert_statement, process, answer_question, save_state, get_last_error


def main():
    time.sleep(5)
    t0 = time.time()
    env = dotenv_values('.env')
    connection = get_connection(
        env['host'],
        env['database'],
        env['user'],
        env['password']
    )
    cursor = connection.cursor()
    init(cursor)
    connection.commit()
    paths = [
        'data/Odata2019File.csv',
        'data/Odata2020File.csv'
    ]
    path, last_count = get_last_error(cursor)
    if path:
        paths = paths[paths.index(path):]
    try:
        for path in paths:
            save_state(path, 'last_path', cursor)
            save_state('0', 'last_row', cursor)
            connection.commit()
            with open(path, encoding='cp1251') as f:
                reader = csv.DictReader(f, delimiter=';')
                insert_statement = generate_insert_statement(reader.fieldnames)
                count = 0
                for row in reader:
                    if not (count < last_count):
                        process(row)
                        row.update(
                            {
                                'year': path \
                                    .replace('data/Odata', '') \
                                    .replace('File.csv', '')
                            }
                        )
                        cursor.execute(insert_statement, row)
                        if count % 1000 == 0:
                            print('saving_state')
                            save_state(count, 'last_row', cursor)
                            connection.commit()
                    count += 1
        connection.commit()
        with open('data/logs.txt', 'w') as f:
            print(
                f'Время выполнения программы составило {(time.time() - t0):.2f} секунд', file=f
            )
        with open('data/result.csv', 'w') as f:
            answer_question(f, cursor)
    except Exception as e:
        with open('data/logs.txt', 'w') as f:
            print(
                f'Произошла ошибка: {traceback.format_exc()}', file=f
            )
        connection.rollback()
    connection.close()


if __name__ == '__main__':
    main()
