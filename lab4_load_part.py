from pymongo import MongoClient
from json import load


def get_database():
    CONNECTION_STRING = "localhost:27017"
    client = MongoClient(CONNECTION_STRING)
    return client['labwork4']


def load_data(filename="data.json"):
    with open(filename) as inFile:
        result = load(inFile)
    return result


if __name__ == "__main__":
    labwork4 = get_database()
    books = labwork4["books"]
    data = load_data()
    books.insert_many(data)
    labwork4.client.close()
