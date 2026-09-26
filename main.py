from library import (
    Book,
    EBook,
    Member,
    Library,
    BookNotAvailableError,
    BorrowLimitExceededError
)


lib = Library()

while True:
    print("\n--- Library Menu ---")
    print("1. Add a Book")
    print("2. Register a Member")
    print("3. Borrow a Book")
    print("4. Return a Book")
    print("5. List Available Books")
    print("6. Search Books")
    print("7. Save Data")
    print("8. Load Data")
    print("9. Exit")

    choice = input("Select an option: ")

    if choice == "1":
        book_type = input("Enter 1 for Physical Book, 2 for EBook: ")
        title = input("Enter title: ")
        author = input("Enter author: ")
        isbn = input("Enter ISBN: ")

        if book_type == "2":
            file_size = input("Enter file size (MB): ")
            link = input("Enter download link: ")
            book = EBook(title, author, isbn, file_size, link)
        else:
            book = Book(title, author, isbn)

        lib.add_book(book)
        print("Book added!")

    elif choice == "2":
        name = input("Enter member name: ")
        member_id = input("Enter member ID: ")
        member = Member(name, member_id)
        lib.register_member(member)
        print("Member registered!")

    elif choice == "3":
        member_id = input("Enter member ID: ")
        isbn = input("Enter book ISBN: ")
        try:
            lib.borrow_book(member_id, isbn)
            print("Check complete.")
        except (BorrowLimitExceededError, BookNotAvailableError) as e:
            print(f"Error: {e}")

    elif choice == "4":
        member_id = input("Enter member ID: ")
        isbn = input("Enter book ISBN: ")
        lib.return_book(member_id, isbn)

    elif choice == "5":
        available = lib.list_available_books()
        if not available:
            print("No available books.")
        else:
            for book in available:
                print(book.get_info())

    elif choice == "6":
        query = input("Enter title or author to search: ")
        results = lib.search_books(query)
        if not results:
            print("No matching books found.")
        else:
            for book in results:
                print(book.get_info())

    elif choice == "7":
        lib.save_to_json("data.json")
        print("Data saved!")

    elif choice == "8":
        lib.load_from_json("data.json")
        print("Data loaded!")

    elif choice == "9":
        print("Goodbye!")
        break

    else:
        print("Invalid option, please try again.")
