import json
import os


class BookNotAvailableError(Exception):
    """raise an error when a book is already borrowed"""
    pass


class BorrowLimitExceededError(Exception):
    """raise an error when member tries to borrow more than 3 books"""
    pass


class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self. isbn = isbn
        self._is_available = True  # private attribute for encapsulation

    # getter to access priv attribute
    @property
    def is_available(self):
        return self._is_available

    def get_info(self):
        """returns formatted string with book details"""
        return f"{self.title} by {self.author}, ISBN: {self.isbn}, Available: {self.is_available}"

    def __str__(self):
        return f"{self.title} by {self.author}"

# EBook INHERITS from Book


class EBook(Book):
    def __init__(self, title, author, isbn, file_size, download_link):
        super().__init__(title, author, isbn)
        self.file_size = file_size
        self.download_link = download_link

    def get_info(self):
        """returns string that includes file size and dl link"""
        normal_info = super().get_info()
        return f"{normal_info}, Size: {self.file_size}, Link: {self.download_link}"

    @property
    def is_available(self):
        return True


class Member:
    def __init__(self, name, member_id):
        self.name = name
        self.member_id = member_id
        # must encapsulate so external code wont break the only-3-books limit
        self._borrowed_books = []

    @property
    def borrowed_books(self):
        return self._borrowed_books

    def __repr__(self):
        """returns (e.g. Member(name, ID))"""
        return f"Member({self.name}, {self.member_id})"


class Library:
    def __init__(self):
        # using dict for faster searching by id or isbn
        self.books = {}    # { 'isbn': BookObject }
        self.members = {}  # { 'member_id': MemberObject }

    def add_book(self, book):
        """add book object to self.books dictionary"""
        self.books[book.isbn] = book

    def register_member(self, member):
        """add member object to self.members dictionary"""
        self.members[member.member_id] = member

    def borrow_book(self, member_id, isbn):
        """ 
        check if member exists and book exists
        check if len(member.borrowed_books) >= 3 if not, raise BorrowLimitExceededError
        check if book.is_available == True if not, raise BookNotAvailableError
        if all true, add book to member's list then set book.is_available = False
        """
        if member_id in self.members and isbn in self.books:
            member = self.members[member_id]
            book = self.books[isbn]

            if len(member.borrowed_books) >= 3:
                raise BorrowLimitExceededError(
                    "You cannot borrow more than 3 books!")
            elif not book.is_available:
                raise BookNotAvailableError("Book is already checked out!")
            else:
                member.borrowed_books.append(book)
                book._is_available = False
        else:
            print("Invalid ID or ISBN.")

    def list_available_books(self):
        """returns a list of available books"""
        available_books = []
        for book in self.books.values():
            if book.is_available:
                available_books.append(book)
        return available_books

    def search_books(self, search):
        """searches books by title or author"""
        results = []
        search_lowercase = search.lower()

        for book in self.books.values():
            if search_lowercase in book.title.lower() or search_lowercase in book.author.lower():
                results.append(book)
        return results

    def return_book(self, member_id, isbn = None):
        """
        remove from member's list, then set book.is_available = True
        if isbn is provided, return the book that has that isbn
        if isbn not provided, return all books  
        """
        if member_id not in self.members:
            print("Invalid member ID.")
            return

        member = self.members[member_id]

        # Return all books
        if isbn is None:
            if len(member.borrowed_books) == 0:
                print(f"member {member.name} has no books.")
                return

            # Mark all books as available
            for book in member.borrowed_books:
                book._is_available = True

            # Clear member's borrowed book list
            member.borrowed_books.clear()
            print(f"Successfully returned all books for {member.name}")

        # Return a single book
        else:
            if isbn not in self.books[isbn]:
                print("Invalid ISBN.")
                return

            book = self.books[isbn]
            if book in member.borrowed_books:
                member.borrowed_books.remove(book)
                book._is_available = True
                print(f"Succesfully returned {book.title}")
            else:
                print(f"{member.name} does not have this book")

    def save_to_json(self, filename="data.json"):
        """Convert the dictionaries to JSON format and write to file"""
        data = {"books": [], "members": []}

        # 1. Save Books and EBooks
        for book in self.books.values():
            if isinstance(book, EBook):
                data["books"].append({
                    "type": "EBook",
                    "title": book.title,
                    "author": book.author,
                    "isbn": book.isbn,
                    "file_size": book.file_size,
                    "download_link": book.download_link
                })
            else:
                data["books"].append({
                    "type": "Book",
                    "title": book.title,
                    "author": book.author,
                    "isbn": book.isbn,
                    "is_available": book.is_available
                })

        # 2. Save Members
        for member in self.members.values():
            # Basic list of ISBNs using a standard loop
            borrowed_isbns = []
            for book in member.borrowed_books:
                borrowed_isbns.append(book.isbn)

            data["members"].append({
                "name": member.name,
                "member_id": member.member_id,
                "borrowed_isbns": borrowed_isbns
            })

        # Write to file
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    def load_from_json(self, filename="data.json"):
        """Read from file and recreate the Book/EBook/Member objects"""
        try:
            with open(filename, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            print("Data file is not found.")
            return

        # Clear existing data
        self.books = {}
        self.members = {}

        # 1. Load Books
        for b_data in data["books"]:
            if b_data["type"] == "EBook":
                book = EBook(b_data["title"], b_data["author"], b_data["isbn"],
                             b_data["file_size"], b_data["download_link"])
            else:
                book = Book(b_data["title"], b_data["author"], b_data["isbn"])
                book._is_available = b_data["is_available"]

            self.add_book(book)

        # 2. Load Members
        for m_data in data["members"]:
            member = Member(m_data["name"], m_data["member_id"])

            # Standard loop to reconnect the borrowed books
            for isbn in m_data["borrowed_isbns"]:
                book = self.books[isbn]
                member.borrowed_books.append(book)

            self.register_member(member)
