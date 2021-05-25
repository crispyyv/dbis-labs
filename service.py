import csv


def process(row):
    for key in row:
        row[key] = row[key].replace(',', '.')
        if row[key] == 'null':
            row[key] = None


def answer_question(file_obj, client):
    max_ball = client.main.aggregate(
            [
                {"$match": {'UkrTestStatus': 'зараховано'}},
                {"$group": {"_id": "$TestYear", "maximum": {"$max": "$PHYSBALL100"}}},
            ]
    )
    writer = csv.DictWriter(file_obj, fieldnames=["_id", "maximum"])
    writer.writeheader()
    for data in max_ball:
        writer.writerow(data)


def save_state(value, type, client):
    client['metadata'].update({'type': type}, {'type': type, 'value': value}, upsert=True)



def get_last_error(client):
    metadata = client['metadata']
    try:
        last_row = int(metadata.find_one({'type': 'last_row'})['value'])
    except:
        last_row = 0
    try:
        path = metadata.find_one({'type': 'path'})['value']
    except:
        path = None
    return path, last_row

