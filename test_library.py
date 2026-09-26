import pytest
from library import Book, Member, Library, BorrowLimitExceededError, BookNotAvailableError


@pytest.fixture
def setup_data():
    lib = Library()
    book1 = Book("1984", "George Orwell", "111")
    member1 = Member("Alice", "F01")

    lib.add_book(book1)
    lib.register_member(member1)

    return lib, book1, member1


def test_borrow_book_success(setup_data):
    lib, book1, member1 = setup_data

    lib.borrow_book(member1.member_id, book1.isbn)

    assert book1 in member1.borrowed_books
    assert book1.is_available == False


def test_borrow_limit_exceeded(setup_data):
    lib, book1, member1 = setup_data

    # giving alice 3 dummy books
    member1._borrowed_books = ["Book A", "Book B", "Book C"]

    # 2. testing to borrow a 4th book
    with pytest.raises(BorrowLimitExceededError):
        lib.borrow_book(member1.member_id, book1.isbn)


def test_borrow_unavailable_book(setup_data):
    lib, book1, member1 = setup_data

    # alice borrows  book legally (book becomes unavailable)
    lib.borrow_book(member1.member_id, book1.isbn)

    # borrow the SAME book agian
    with pytest.raises(BookNotAvailableError):
        lib.borrow_book(member1.member_id, book1.isbn)


def test_return_book_success(setup_data):
    lib, book1, member1 = setup_data

    # setting up: borrow the book first to have something to return
    lib.borrow_book(member1.member_id, book1.isbn)

    # returning book
    lib.return_book(member1.member_id, book1.isbn)

    # book should be gone from the list and available to borrow again
    assert book1 not in member1.borrowed_books
    assert book1.is_available == True


def test_return_unborrowed_book(setup_data):
    lib, book1, member1 = setup_data

    # try to return a book that was never borrowed
    lib.return_book(member1.member_id, book1.isbn)

    # only need to assert that her list is still empty and the book is still available.
    # (safety checks were written in library.py)

    assert len(member1.borrowed_books) == 0
    assert book1.is_available == True
