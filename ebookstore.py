''' Pseudo code
1. Create database and table - Done
2. Fill database with rows of information - Done
3. Display welcome message and say if table has been found or created.
3. Present user with 5 options: Enter book, Update book, Delete book, Search books, Exit
4. Enter book: Ask user for name, author, qty. Add +1 to previous ID for new ID
5. Update book: Ask user for ID of book to update. Ask user to update Title, Author or Qty
6. Ask user for ID of book to delete. (Keep ID same?)
7. Ask user for name of book to find a specific book
4. Exit closes program and ends DB connection
'''

import sqlite3


def ebookstore():
    """ Function to check for or create ebookstore database and table called books. Table populated with base books"""

    # Create and connect to db
    db = sqlite3.connect('ebookstore')
    cursor = db.cursor()

    # Checks if book table already exists. Displays appropriate message
    cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='books' ''')
    if cursor.fetchone()[0] == 1:
        print("Books table found.")

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
        print("Book table created")

ebookstore()