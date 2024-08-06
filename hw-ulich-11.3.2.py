import json
from abc import ABC, abstractmethod

class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def __str__(self):
        return f"{self.title} by {self.author}"

class Librarian:
    def __init__(self, name):
        self.name = name

class Reader:
    def __init__(self, name):
        self.name = name


class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance.log_file = open('log.txt', 'a')
        return cls._instance

    def log(self, message):
        self.log_file.write(message + '\n')

    def close(self):
        self.log_file.close()


class LibraryRepository:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)
        Logger().log(f"Added book: {book}")

    def remove_book(self, title):
        self.books = [b for b in self.books if b.title != title]
        Logger().log(f"Removed book: {title}")

    def get_all_books(self):
        return self.books

    def save_to_file(self):
        with open('books.json', 'w') as f:
            json.dump([{"title": b.title, "author": b.author} for b in self.books], f)
            Logger().log("Saved books to file")

    def load_from_file(self):
        try:
            with open('books.json', 'r') as f:
                books_data = json.load(f)
                self.books = [Book(b["title"], b["author"]) for b in books_data]
                Logger().log("Loaded books from file")
        except FileNotFoundError:
            Logger().log("File not found for loading books")

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class AddBookCommand(Command):
    def __init__(self, repository, book):
        self.repository = repository
        self.book = book

    def execute(self):
        self.repository.add_book(self.book)

class Observer(ABC):
    @abstractmethod
    def update(self, message):
        pass

class BookObserver(Observer):
    def update(self, message):
        print(f"Notification: {message}")

class SearchStrategy(ABC):
    @abstractmethod
    def search(self, books, query):
        pass

class TitleSearch(SearchStrategy):
    def search(self, books, query):
        return [b for b in books if query.lower() in b.title.lower()]

class AuthorSearch(SearchStrategy):
    def search(self, books, query):
        return [b for b in books if query.lower() in b.author.lower()]

# Пример
if __name__ == "__main__":
    repository = LibraryRepository()
    repository.load_from_file()

    librarian = Librarian("Alice")
    reader = Reader("Bob")

    command = AddBookCommand(repository, Book("The Catcher in the Rye", "J.D. Salinger"))
    command.execute()

    search_strategy = TitleSearch()
    results = search_strategy.search(repository.get_all_books(), "Catcher")
    print("Search results:", results)

    repository.save_to_file()


# Используемые паттерны проектирования

# 1. **Singleton** - для класса `Logger`
#    - Паттерн Singleton гарантирует, что у вас будет только один экземпляр логгера, и предоставляет глобальную точку
#    доступа к нему. Это помогает централизовать логи приложения и избежать создания нескольких экземпляров логгера.
#
# 2. **Factory Method** - для создания объектов сущностей
#    - Использование фабричного метода позволяет инкапсулировать создание объектов (например, книг, читателей и библиотекарей)
#    и предоставляет возможность легко изменять и расширять код, создавая новые классы, не влияя на существующий код.
#
# 3. **Repository** - для управления доступом к данным
#    - С помощью репозитория можно абстрагироваться от деталей хранения и извлечения объектов. Это позволяет легко менять
#    способ хранения информации (в памяти, в базе данных, в файлах) без изменения остальной части приложения.
#
# 4. **Command** - для выполнения действий с сущностями
#    - Паттерн Command позволяет инкапсулировать запросы как объекты, что помогает реализовать возможность отмены действий
#    и позволяет легко добавлять новые операции без изменения существующих классов.
#
# 5. **Observer** - для уведомления о изменениях
#    - Паттерн Observer может быть использован для уведомления слушателей о каких-либо изменениях в сущностях (например,
#    добавить событие "книга добавлена"), что позволяет отслеживать состояние приложения без сильной связности.
#
# 6. **Strategy** - для реализации различных методов поиска
#    - Этот паттерн позволяет определить семейство алгоритмов поиска, инкапсулировать их и делать их взаимозаменяемыми.
#    Это может быть полезно при добавлении новых стратегий поиска, например, по автору, названию или жанру.
