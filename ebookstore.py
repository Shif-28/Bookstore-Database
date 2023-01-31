''' Pseudo code
1. Create database and table - Done
2. Fill database with rows of information - Done
3. Define functions for the following 6 options:
3a. View all: Show all books in tabulate - Done
3b. Enter book: Ask user for name, author, qty. Add +1 to previous ID for new ID - Done
3c. Update book: Ask user for ID of book to update. Ask user to update Title, Author or Qty
3d. Ask user for ID of book to delete. (Keep ID same?)
3e. Ask user for name of book to find a specific book
3f. Exit closes program and ends DB connection
4. Display welcome message and say if table has been found or created. Use tabulate module for formatting
5. Present user with 5 options: Enter book, Update book, Delete book, Search books, Exit

'''

import sqlite3
from tabulate import tabulate

def ebookstore():
    """ Check for or create table called books. Table populated with base books"""

    # Checks if book table already exists. Displays appropriate message
    cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='books' ''')
    if cursor.fetchone()[0] == 1:
        print("Books table found\n")

    # If no book table, create new book table and add base book information
    else:
        cursor.execute('''
            CREATE TABLE books(id INTEGER PRIMARY KEY, Title TEXT, Author TEXT, Qty INTEGER)
        ''')
        db.commit()

        # Base books to add to table
        base_books = [
            (3001, 'A Tale of Two Cities', 'Charles Dickens', 30),
            (3002, 'Harry Potter and the Philosopher Stone\'s', 'J.K. Rowling', 40),
            (3003, 'The Lion, the Witch and the Wardrobe', 'C.S. Lewis', 25),
            (3004, 'The Lord of the Rings', 'J.R.R Tolkien', 37),
            (3005, 'Alice in Wonderland', 'Lewis Carroll', 12)
            ]

        # Insert base books info into table
        insert_base_books = '''INSERT INTO books(id, Title, Author, Qty) VALUES(?, ?, ?, ?)'''
        cursor.executemany(insert_base_books, base_books)
        db.commit()
        print("Book table created\n")

def view_all():
    """ Display all rows in books table"""

    cursor.execute('''SELECT * FROM books''')
    rows = cursor.fetchall()
    print(tabulate(rows, headers=["Book ID", "Book Name", "Book Author", "QTY"], tablefmt="rounded_grid"))

def add_book():
    """ Add book to database with unique id number"""

    # Request book information from user
    book_name = input("Please enter the name of the book: ")
    book_author = input("Please enter the author of the book: ")
    while True:
        try:
            book_qty = int(input("PLease enter the current quantity of the book: "))
            break
        except ValueError:
            print("That was the wrong input. Try again")

    # Create new unique id and new book variable
    cursor.execute(''' SELECT MAX(id) FROM books ''')
    max_id = (cursor.fetchone())
    new_id = sum(max_id) + 1
    new_book = [(new_id, book_name, book_author, book_qty)]

    # Insert new book to table
    insert_new_book = '''INSERT INTO books (id, Title, Author, Qty) VALUES(?, ?, ?, ?)'''
    cursor.executemany(insert_new_book, new_book)
    db.commit()


# Create and connect to db
db = sqlite3.connect('ebookstore')
cursor = db.cursor()

ebookstore()
'''add_book()'''
view_all()





''' add welcome message'''
'''ebookstore()'''
'''Provide options'''