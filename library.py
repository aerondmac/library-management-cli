class BookNotAvailableError(Exception):
    """raise an error when a book is already borrowed."""
    pass


class BorrowLimitExceededError(Exception):
    """raise an error when member tries to borrow more than 3 books."""
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
        pass

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
        pass

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
        pass


class Library:
    def __init__(self):
        # using dict for faster searching by id or isbn
        self.books = {}    # { 'isbn': BookObject }
        self.members = {}  # { 'member_id': MemberObject }

    def add_book(self, book):
        """add book object to self.books dictionary"""
        self.books[book.isbn] = book

    def register_member(self, member):
        """add member object to self.members dictionary."""
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

    def return_book(self, member_id, isbn):
        """remove from member's list, then set book.is_available = True"""
        if member_id in self.members and isbn in self.books:
            member = self.members[member_id]
            book = self.books[isbn]

            member.borrowed_books.remove(book)
            book._is_available = True

    def save_to_json(self, filename="data.json"):
        """Convert the dictionaries to JSON format and write to file"""
        pass

    def load_from_json(self, filename="data.json"):
        """Read from file and recreate the Book/EBook/Member objects"""
        pass
