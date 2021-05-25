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
    client = get_connection(
        env['host'],
        env['database']
    )
    init(client)
    paths = [
        'data/Odata2019File.csv',
        'data/Odata2020File.csv'
    ]
    path, last_count = get_last_error(client)
    if path:
        paths = paths[paths.index(path):]
    tmp = []
    try:
        for path in paths:
            save_state(path, 'last_path', client)
            save_state(0, 'last_row', client)
            with open(path, encoding='cp1251') as f:
                reader = csv.DictReader(f, delimiter=';')
                count = 0
                for row in reader:
                    if not (count < last_count):
                        process(row)
                        row.update(
                            {
                                'year': path.replace('data/Odata', '').replace('File.csv', '')
                            }
                        )
                        tmp.append(row)
                        if count % 1000 == 0:
                            print('saving_state')
                            client['data'].insert_many(tmp)
                            save_state(count, 'last_row', client)
                            tmp = []
                    count += 1
        with open('data/logs.txt', 'w') as f:
            print(
                f'Время выполнения программы составило {(time.time() - t0):.2f} секунд', file=f
            )
        with open('data/result.csv', 'w') as f:
            answer_question(f, client)
    except Exception as e:
        with open('data/logs.txt', 'w') as f:
            print(
                f'Произошла ошибка: {traceback.format_exc()}', file=f
            )


if __name__ == '__main__':
    main()
