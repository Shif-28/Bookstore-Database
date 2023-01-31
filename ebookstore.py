import sqlite3
from tabulate import tabulate


def ebookstore():
    """ Check for or create table called books. Table populated with base books """

    # Checks if book table already exists. Displays appropriate message
    cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type = 'table' AND name = 'books' ''')
    if cursor.fetchone()[0] == 1:
        print("\n≡ Existing Books table has been found ≡\n")

    # If no book table, create new book table and add base book information. Text is case-insensitive.
    else:
        cursor.execute('''
            CREATE TABLE books(
            id INTEGER PRIMARY KEY, Title TEXT COLLATE NOCASE, Author TEXT COLLATE NOCASE, Qty INTEGER)
        ''')

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
        print("\n≡ A new Books table has been created ≡\n")


def view_all():
    """ Display all rows in books table """

    cursor.execute('''SELECT * FROM books''')
    rows = cursor.fetchall()
    print(82 * "═")
    print("\t\t\t\t\t\t\t📘 All Database Books 📙")
    print(82 * "═")
    print(tabulate(rows, headers=["Book ID", "Book Name", "Book Author", "QTY"], tablefmt="rounded_grid"))
    print(82 * "═")


def add_book():
    """ Add book to database with unique id number """

    # Request book information from user
    book_name = input("🔲 Please enter the name of the book: ")
    book_author = input("🔲 Please enter the author of the book: ")
    while True:
        try:
            book_qty = int(input("🔲 Please enter the current quantity of the book: "))
            break
        except ValueError:
            print("\n❌ That was the wrong input. Try again\n")

    # Create new unique id and new book variable
    cursor.execute(''' SELECT MAX(id) FROM books ''')
    max_id = (cursor.fetchone())
    new_id = sum(max_id) + 1
    new_book = [(new_id, book_name, book_author, book_qty)]

    # Insert new book to table
    sql_insert_new_book = '''INSERT INTO books(id, Title, Author, Qty) VALUES(?, ?, ?, ?)'''
    cursor.executemany(sql_insert_new_book, new_book)
    db.commit()
    print("\n✅ Book added to the Books table.\n")


def update_book():
    """ Update book information for the users choice of book """

    # Ask user which book to update and check if book id exists in database
    while True:
        try:
            update_book_id = int(input("\n🔲 Enter the ID of the book you want to update: "))
            cursor.execute('''SELECT id FROM books WHERE id=?''', (update_book_id,))
            check_id = cursor.fetchone() is not None
            if check_id:
                print("\n✅ The following Book was found in the Database:")
                cursor.execute('''SELECT id, Title, Author, Qty FROM books WHERE id=?''', (update_book_id,))
                display_id = cursor.fetchall()
                print(tabulate(display_id, headers=["Book ID", "Book Name", "Book Author", "QTY"],
                               tablefmt="rounded_grid"))
                break
            while True:
                if not check_id:
                    print("\n❌ Book not found in Database. Try again")
                    break
        except ValueError:
            print("\n❌ That was the wrong input. Try again")

    # Ask user what information to update
    while True:
        try:
            update_choice = int(input("\n≡ Enter an option number below:"
                                      "\n🔲 1 - Update book name"
                                      "\n🔲 2 - Update book author name"
                                      "\n🔲 3 - Update book qty"
                                      "\n❌ 4 - Back to menu"
                                      "\nEnter Option: "))
            break
        except ValueError:
            print("\n❌ That was the wrong input. Try again")

    while True:
        # Update book name
        if update_choice == 1:
            update_book_name = input("\n🔲 Enter new book name: ")
            print()
            cursor.execute('''UPDATE books SET Title = ? WHERE id = ?''', (update_book_name, update_book_id))
            db.commit()
            break

        # Update book author name
        elif update_choice == 2:
            update_book_author = input("\n🔲 Enter new author name:")
            print()
            cursor.execute('''UPDATE books SET Author = ? WHERE id = ?''', (update_book_author, update_book_id))
            db.commit()
            break

        # Update book qty
        elif update_choice == 3:
            update_book_qty = input("\n🔲Enter new qty:")
            print()
            cursor.execute('''UPDATE books SET Qty = ? WHERE id = ?''', (update_book_qty, update_book_id))
            db.commit()
            break

        # Return to main menu
        elif update_choice == 4:
            print("\n❌ Returning to main menu\n")
            break


def delete_book():
    """ Deletes the users choice of book from the database """

    # Asks user which book to delete and check if book exists in database
    while True:
        try:
            delete_book_id = int(input("\n🔲 Enter the ID of the book you want to delete: "))
            cursor.execute('''SELECT id FROM books WHERE id=?''', (delete_book_id,))
            check_id = cursor.fetchone() is not None
            if check_id:
                print("\n✅ The following Book was found in the Database.")
                cursor.execute('''SELECT id, Title, Author, Qty FROM books WHERE id=?''', (delete_book_id,))
                display_id = cursor.fetchall()
                print(tabulate(display_id, headers=["Book ID", "Book Name", "Book Author", "QTY"],
                               tablefmt="rounded_grid"))
                break
            while True:
                if not check_id:
                    print("\n❌ Book not found in Database. Try again")
                    break
        except ValueError:
            print("\n❌ That was the wrong input. Try again")

    # Asks user to confirm deletion. Then deletes book from database
    while True:
        try:
            delete_choice = int(
                input("\n≡ Are you sure you want to delete this book from the database? Enter an option number below:"
                      "\n✅ 1 - Yes"
                      "\n❌ 2 - No"
                      "\nEnter option: "))
            if delete_choice == 1:
                cursor.execute('''DELETE FROM books where id=?''', (delete_book_id,))
                print("\n✅ Book has been deleted from the database\n")
                db.commit()
                break
            elif delete_choice == 2:
                print("\n❌ You chose to not delete the book. Returning to menu\n")
                break
            while True:
                if delete_choice != 1 or delete_choice != 2:
                    print("\n❌ That is not a valid answer. Try again")
                    break
        except ValueError:
            print("\n❌ That was the wrong input. Try again")


def search_book():
    """ User enters ID of book they want to see """

    # Asks user to search for book by ID, book name or author
    while True:
        try:
            search_choice = int(input("\n≡ Enter the search option number from below: "
                                      "\n🔲 1 - Search with ID of book"
                                      "\n🔲 2 - Search with Name of book"
                                      "\n🔲 3 - Search with Name of book's author"
                                      "\n❌ 4 - Back to menu"
                                      "\nEnter option: "))
            break
        except ValueError:
            print("\n❌ That was the wrong input. Try again")

    while True:
        # Search with ID of book
        if search_choice == 1:
            try:
                search_book_id = int(input("\n🔲 Enter the ID of the book you want to see: "))
                cursor.execute('''SELECT id FROM books WHERE id=?''', (search_book_id,))
                check_id = cursor.fetchone() is not None
                if check_id:
                    print("\n✅ The following book was found in the Database.")
                    cursor.execute('''SELECT id, Title, Author, Qty FROM books WHERE id=?''', (search_book_id,))
                    display_search_id = cursor.fetchall()
                    print(tabulate(display_search_id, headers=["Book ID", "Book Name", "Book Author", "QTY"],
                                   tablefmt="rounded_grid"))
                    print()
                    break
                while True:
                    if not check_id:
                        print("\n❌ Book not found in Database. Try again")
                        break
            except ValueError:
                print("\n❌ That was the wrong input. Try again")

        # Search with name of book
        elif search_choice == 2:
            search_book_name = input("\n🔲 Enter the name of the book you want to see: ")
            cursor.execute('''SELECT Title FROM books WHERE Title=?''', (search_book_name,))
            check_name = cursor.fetchone() is not None
            if check_name:
                print("\n✅ The following book was found in the Database.")
                cursor.execute('''SELECT id, Title, Author, Qty FROM books WHERE Title=?''', (search_book_name,))
                display_search_name = cursor.fetchall()
                print(tabulate(display_search_name, headers=["Book ID", "Book Name", "Book Author", "QTY"],
                               tablefmt="rounded_grid"))
                print()
                break
            while True:
                if not check_name:
                    print("\n❌Book not found in Database. Try again")
                    break

        # Search with name of author
        elif search_choice == 3:
            search_book_author = input("\n🔲 Enter the authors name: ")
            cursor.execute('''SELECT Author FROM books WHERE Author=?''', (search_book_author,))
            check_author = cursor.fetchone() is not None
            if check_author:
                print("\n✅ The following book was found in the Database.")
                cursor.execute('''SELECT id, Title, Author, Qty FROM books WHERE Author=?''', (search_book_author,))
                display_search_author = cursor.fetchall()
                print(tabulate(display_search_author, headers=["Book ID", "Book Name", "Book Author", "QTY"],
                               tablefmt="rounded_grid"))
                print()
                break
            while True:
                if not check_author:
                    print("\n❌ Book not found in Database. Try again")
                    break

        # Return to main menu
        elif search_choice == 4:
            print("\n❌ Returning to main menu\n")
            break


# Create and connect to db
db = sqlite3.connect('ebookstore')
cursor = db.cursor()

print(42 * "═")
print("📘 Welcome to the eBookstore Database! 📙")
print(42 * "═")
ebookstore()

# Menu options for user to select. Call relevant function.
while True:
    menu = input("≡ Please choose an option number from the list below:"
                 "\n🔲 1 - View all books"
                 "\n🔲 2 - Add a new book"
                 "\n🔲 3 - Update an existing books details"
                 "\n🔲 4 - Delete an existing book"
                 "\n🔲 5 - Search for a book"
                 "\n❌ 6 - Exit the database"
                 "\n\nEnter Option: ")

    if menu == "1":
        view_all()

    elif menu == "2":
        add_book()

    elif menu == "3":
        update_book()

    elif menu == "4":
        delete_book()

    elif menu == "5":
        search_book()

    elif menu == "6":
        print("\nBye!")
        db.close()
        exit()

    else:
        print("\n❌ That is the wrong input. Please try again.\n")
