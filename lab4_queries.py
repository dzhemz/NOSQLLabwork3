from pymongo import MongoClient
import math


def get_database():
    CONNECTION_STRING = "localhost:27017"
    client = MongoClient(CONNECTION_STRING)
    return client['labwork4']


def selection_by_genre(genre, books_):
    return books_.find({"genre": {"$in": [genre]}})


def selection_by_author(author, books_):
    return books_.find({"author": {"$eq": author}})


def order_by_postponed(books_):
    return sorted(books_.find(), key=lambda book: -int(book["postponed"]))


# определить среднее значение читающих книгу
# определить среднее значение оставивших книгу
# определить среднее значение отложивших книгу
def medium_values(books_):
    readers = 0
    postponed = 0
    notFinished = 0
    for book in books.find():
        readers += int(book.get("readers"))
        postponed += int(book.get("postponed"))
        notFinished += int(book.get("notFinished"))

    return [round(readers / 210), round(postponed / 210), round(notFinished / 210)]


def most_interesting(books_):
    return max(
        books_.find(),
        key=lambda book: int(book["readers"]) * math.log(int(book["postponed"]) + 5) / (1 + int(book["notFinished"])))


# топ 10 книг, которые были прочитанны больше всего
def top_10_read_books(books_):
    return sorted(books.find(), key=lambda book: -int(book["read"]))[:10]


if __name__ == "__main__":
    labwork4 = get_database()
    books = labwork4["books"]
    # selection_by_genre("Фантастика", books)
    # selection_by_author("Владимир Левендорский", books)
    # order_by_postponed(books)
    # medium_values(books)
    # most_interesting(books)
    # top_10_read_books(books)
    labwork4.client.close()
