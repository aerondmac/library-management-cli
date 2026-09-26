# Library Management CLI

A command-line app built in Python to manage library books, e-books, and members using OOP, custom exceptions, JSON storage, and pytest.

## How to Run
Run the app:
    python main.py

Run the unit tests:
    python -m pytest test_library.py

## Example Usage
    1. Add a Book
    2. Register a Member
    3. Borrow a Book
    4. Return a Book
    5. List Available Books
    6. Search Books
    7. Save & Exit
    Select an option: 1
    Enter title: 1984
    Enter author: George Orwell
    Enter ISBN: 111
    Book added!


## Reflection
The hardest part of this project was learning pytest from scratch, especially understanding how fixtures work and whenand how to use pytest.raises for custom exceptions versus normal assert statements. While writing the Library methods, I had to debug method indentation errors, missing .lower() calls for title searches to not make them case-sensitive, and accidentally looping over self.books dictionary keys instead of .values() when trying to access book objects. Also, getting used to the Git feature-branch workflow, remembering to link GitHub issues in pull request descriptions, and struggling to figure out how to serialize custom objects into JSON were major challenges. I used inheritance by having EBook inherit from Book with super().__init__() so I did not have to rewrite the title, author, and ISBN attributes. For polymorphism, I overrode the is_available property in EBook to always return True and used super().get_info() in EBook.get_info() to attach the file size and download link. To improve the project, I'd finish the JSON storage and add due dates using datetime module to calculate late return fees.