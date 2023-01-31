''' Pseudo code
1. Create database and table - Done
2. Fill database with rows of information - Done
3. Define functions for the following 6 options:
3a. View all: Show all books in tabulate - Done
3b. Enter book: Ask user for name, author, qty. Add +1 to previous ID for new ID - Done
3c. Update book: Ask user for ID of book to update. Ask user to update Title, Author or Qty - Done
3d. Ask user for ID of book to delete. - Done
3e. Ask user for name of book to find a specific book
3f. Exit closes program and ends DB connection
4. Display welcome message and say if table has been found or created. Use tabulate module for formatting
5. Present user with 5 options: Enter book, Update book, Delete book, Search books, Exit

'''

import sqlite3
from tabulate import tabulate


def ebookstore():
    """ Check for or create table called books. Table populated with base books """

    # Checks if book table already exists. Displays appropriate message
    cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type = 'table' AND name = 'books' ''')
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
        sql_insert_base_books = '''INSERT INTO books(id, Title, Author, Qty) VALUES(?, ?, ?, ?)'''
        cursor.executemany(sql_insert_base_books, base_books)
        db.commit()
        print("Books table created\n")


def view_all():
    """ Display all rows in books table """

    cursor.execute('''SELECT * FROM books''')
    rows = cursor.fetchall()
    print(tabulate(rows, headers=["Book ID", "Book Name", "Book Author", "QTY"], tablefmt="rounded_grid"))


def add_book():
    """ Add book to database with unique id number """

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
    sql_insert_new_book = '''INSERT INTO books(id, Title, Author, Qty) VALUES(?, ?, ?, ?)'''
    cursor.executemany(sql_insert_new_book, new_book)
    db.commit()
    print("Book added to the Books table")


def update_book():
    """ Update book information for the users choice of book """

    # Ask user which book to update and check if book id exists in database
    while True:
        try:
            update_book_id = int(input("Enter the ID of the book you want to update: "))
            cursor.execute('''SELECT id FROM books WHERE id=?''', (update_book_id,))
            check_id = cursor.fetchone() is not None
            if check_id == True:
                print("\nThe following Book was found in the Database.")
                cursor.execute('''SELECT id, Title, Author, Qty FROM books WHERE id=?''', (update_book_id,))
                display_id = cursor.fetchall()
                print(tabulate(display_id, headers=["Book ID", "Book Name", "Book Author", "QTY"],
                               tablefmt="rounded_grid"))
                break
            while True:
                if check_id == False:
                    print("\nBook not found in Database. Try again\n")
                    break
        except ValueError:
            print("\nThat was the wrong input. Try again\n")

    # Ask user what information to update
    while True:
        try:
            update_choice = int(input("\nEnter an option number below:"
                                      "\n1 - Update book name"
                                      "\n2 - Update book author name"
                                      "\n3 - Update book qty"
                                      "\n4 - Back to menu"
                                      "\nEnter Option: "))
            break
        except ValueError:
            print("\nThat was the wrong input. Try again\n")

    while True:
        # Update book name
        if update_choice == 1:
            update_book_name = input("Enter new book name: ")
            cursor.execute('''UPDATE books SET Title = ? WHERE id = ?''', (update_book_name, update_book_id))
            db.commit()
            break

        # Update book author name
        elif update_choice == 2:
            update_book_author = input("Enter new author name: ")
            cursor.execute('''UPDATE books SET Author = ? WHERE id = ?''', (update_book_author, update_book_id))
            db.commit()
            break

        # Update book qty
        elif update_choice == 3:
            update_book_qty = input("Enter new qty: ")
            cursor.execute('''UPDATE books SET Qty = ? WHERE id = ?''', (update_book_qty, update_book_id))
            db.commit()
            break

        # Return to main menu
        elif update_choice == 4:
            print("\nReturning to main menu\n")
            break


def delete_book():
    while True:
        try:
            delete_book_id = int(input("Enter the ID of the book you want to delete: "))
            cursor.execute('''SELECT id FROM books WHERE id=?''', (delete_book_id,))
            check_id = cursor.fetchone() is not None
            if check_id == True:
                print("\nThe following Book was found in the Database.")
                cursor.execute('''SELECT id, Title, Author, Qty FROM books WHERE id=?''', (delete_book_id,))
                display_id = cursor.fetchall()
                print(tabulate(display_id, headers=["Book ID", "Book Name", "Book Author", "QTY"],
                               tablefmt="rounded_grid"))
                break
            while True:
                if check_id == False:
                    print("\nBook not found in Database. Try again\n")
                    break
        except ValueError:
            print("\nThat was the wrong input. Try again\n")

    # Asks user to confirm deletion. Then deletes book from database
    while True:
        try:
            delete_choice = int(
                input("\nAre you sure you want to delete this book from the database? Enter an option number below:"
                      "\n1 - Yes"
                      "\n2 - No"
                      "\nEnter option: "))
            if delete_choice == 1:
                cursor.execute('''DELETE FROM books where id=?''', (delete_book_id,))
                print("\nBook has been deleted from the database")
                db.commit()
                break
            elif delete_choice == 2:
                print("\nYou chose to not delete the book. Returning to menu")
                break
            while True:
                if delete_choice != 1 or delete_choice != 2:
                    print("\nThat is not a valid answer. Try again")
                    break
        except ValueError:
            print("\nThat was the wrong input. Try again\n")


# Create and connect to db
db = sqlite3.connect('ebookstore')
cursor = db.cursor()

ebookstore()
'''add_book()'''
'''view_all()'''
'''update_book()'''
'''delete_book()'''

''' add welcome message'''
'''ebookstore()'''
'''Provide options'''
