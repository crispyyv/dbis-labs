import pymongo


def get_connection(host, database):
    return pymongo.MongoClient(
        host,
        27017)[database]
