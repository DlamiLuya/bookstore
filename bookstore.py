from tabulate import tabulate
import pandas as pd
import sqlite3
db = sqlite3.connect(r'c:\Users\dlami\Desktop\Hyperion\Level2\L2T13\\ebookstore.db')
cursor = db.cursor()

#Create a database table that for the bookstore
cursor.execute('''
    CREATE TABLE IF NOT EXISTS book(id INTEGER PRIMARY KEY,
               title TEXT,
               author TEXT, 
               qty INTEGER)
''')
db.commit() 

#initialise the database table with values.
initial_books = [(3001, 'A Tale of Two Cities', 'Charles Dickens', 30),(3002, 'Harry Potter and the Philosopher\'s Stone', 'J.K. Rowling', 40),(3003, 'The Lion, the Witch and the Wardrobe', 'C. S. Lewis', 25),(3004, 'The Lord of the Rings', 'J.R.R Tolkien', 37),(3005, 'Alice in Wonderland', 'Lewis Carroll', 12)]
cursor = db.cursor()
cursor.executemany('''INSERT or REPLACE INTO book(id,title,author,qty)  VALUES(?,?,?,?)''', initial_books)
print('values inserted to the database\n')
db.commit()

# Define a function that will allow user to enter a new book to a database.
def enter_book():
    book_title = input("Book title: ") # Prompt user to enter book details.
    book_author = input("Book author: ")
    while True:
        try:
            book_qty = int(input("Book Quantity: "))
            break
        except ValueError:
            print("oops quantity can only be a number\n")

    cursor.execute('''SELECT MAX(id) FROM book''') # Get the maximum id record from the databse.
    id = cursor.fetchone()
    # Enter the data input by user and from the max id add 1 to make a new book id and record on  a variable.
    record = [int(id[0] + 1), book_title, book_author, book_qty]
    cursor.execute('''INSERT INTO book(id,title,author,qty) VALUES(?,?,?,?)''', record)# add the record to the database and commit.
    db.commit()
    # Print relevant message.
    print('Book entered into database.\n')


# Define a function that will allow a user to update/modify data about a book that already exists in the database.
def update_book():
    print(pd.read_sql_query('SELECT * FROM book', db))
    print('\n')
    while True:
        try: # Try/except block to ensure that the user enteres integer values when prompted.
            # Prompt user to enter the book id they would like to update as well as the new book quantity.
            book_id = int(input("Enter book id you'd like to change: "))
            book_qty = int(input("Change book quantity: "))
            break
        except ValueError:
            print("oops quantity and id can only be a number\n")

    # Update the book database and commit.
    cursor.execute('''UPDATE book SET qty = ? WHERE id = ? ''', (book_qty,book_id))
    db.commit()
    # Print relevant message.
    print("Book quantity updated\n")


# Define a function that will allow a user to delete a book from the database.
def delete_book():
    while True:
        try:
            # Prompt user to enter book id they would like to delete.
            book_id = int(input("Enter book id you would like to delete: "))
            break
        except ValueError:
            print("oops id can only be a number.\n")

    try: # try/except block to ensure tht the user inputs a valid book. 
        # fetch the book the user chose and delete it from the database.      
        cursor.execute('''SELECT * FROM book WHERE id = ? ''', (book_id,))
        book = cursor.fetchone()
        cursor.execute('''DELETE FROM book WHERE id = ? ''', (book_id,))
        db.commit()
        print(f'''Title: {book[1]}
by: {book[2]}
Has been deleted''')
    except TypeError:
        print("Sorry it seems we don't have that book.\n")



# Define a function that will allow a user to search for a specific book in the database.
def search_book():
    while True:
        # Prompt user to choose how they would like to search for a book using menu option.
        searchby = input('''\nSearch by:
t - book title
a - book author
id - book id
choose one of the above options: ''')

        if searchby == "t":
            try:# try/except block for if book doesnt exist on the database.
                # Prompt user to enter title and use it to search for book and print it out in a user friendly way.
                book_title = input("Enter book title")
                cursor.execute('''SELECT * FROM book WHERE title =?''', (book_title,))
                book = cursor.fetchone()
                print(f'''BOOK:
Title:  {book[1]}
Author: {book[2]}
ID:     {book[0]}''')
                break
            except TypeError:
                print("We do not have that book")
                break

        elif searchby == "a":
            try:# try/except block for if book doesnt exist on the database.
                # Prompt user to enter author and use it to search for book and print it out in a user friendly way.
                book_author = input("Enter book author")
                cursor.execute('''SELECT * FROM book WHERE author =?''', (book_author,))
                book = cursor.fetchone()
                print(f'''BOOK:
Title:  {book[1]}
Author: {book[2]}
ID:     {book[0]}''')
                break
            except TypeError:
                print("We do not have that author with us.")
                break

        elif searchby == "id":
            try:# try/except block for if book doesnt exist on the database.
                # Prompt user to enter id and use it to search for book and print it out in a user friendly way.
                book_id = input("Enter book id")
                cursor.execute('''SELECT * FROM book WHERE id = ?''', (book_id,))
                book = cursor.fetchone()
                print(f'''BOOK:
Title:  {book[1]}
Author: {book[2]}
ID:     {book[0]}''')
                break
            except TypeError:
                print("That book id doesnt exist.\n")
                break

        else:
            print("Invalid option. please try again.\n")


# Define a function that will allow the user to view all books within the database.
def view_books():
    # Print the database table.
    print(pd.read_sql_query('SELECT * FROM book', db)
          )
    print('\n')

# A menu that will direct the use of the app to the user.
while True:
    # Menu that gives user option to choose what they would like to do.
    menu = input('''\n1. Enter book
2. Update book
3. Delete book
4. Search books
5. View all books
0. Exit
choose a selection from the menu:  ''')
    # call each of the defined functions relevantly to the option chosen by the user. 
    if menu == '1':
        enter_book()

    elif menu == '2':
        update_book()

    elif menu == '3':
        delete_book( )

    elif menu == '4':
        search_book()

    elif menu == '5':
        view_books()

    elif menu == '0':
        db.close()
        print('Goodbye')
        exit()

    else:
        print("You have entered an invalid option. Try again\n")
