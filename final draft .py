import matplotlib.pyplot as plt    # Import library to create charts and graphs
import pandas as pd                # Import library to handle data tables easily
import tkinter as tk               # Import library to create the visual window (GUI)
from tkinter import simpledialog   # Tool to pop up boxes asking for text input
from tkinter import messagebox     # Tool to pop up boxes showing messages or alerts

# ===================== CREATE DATA FILES =====================

open("books.txt", "a").close()            # Creates the books file if it doesn't exist
open("borrow_records.txt", "a").close()   # Creates the borrowing record file if it doesn't exist


# ===================== FILE HANDLING =====================

def load_books(filename):           # Function to read data from a file into the program
    books = []                      # Start with an empty list to hold book data
    file = open(filename, "r")      # Open the file in 'read' mode

    for line in file:               # Look at every line in the file one by one
        if line.strip():            # If the line isn't empty:
            books.append(line.strip().split(","))  # Clean the line and split it into parts by commas

    file.close()                                    # Close the file to save memory
    return books                                    # Give the list of books back to the program


def edit_books(filename, books):  # Function to save/overwrite the file with new data
    file = open(filename, "w")  # Open the file in 'write' mode (erases old content)

    for book in books:  # For every book in our list:
        file.write(",".join(book) + "\n")  # Combine the parts with commas and write to a new line

    file.close()  # Close the file to finish saving


# ===================== ADD BOOK =====================

def gui_add_book():  # Function to show a form for adding a new book
    title = simpledialog.askstring("Add Book", "Title")       # Ask user for the book title
    book_id = simpledialog.askstring("Add Book", "Book ID")   # Ask user for the unique ID
    author = simpledialog.askstring("Add Book", "Author")     # Ask user for the author name
    year = simpledialog.askstring("Add Book", "Year")         # Ask user for the publication year
    subject = simpledialog.askstring("Add Book", "Subject")   # Ask user for the book category
    section = simpledialog.askstring("Add Book", "Section")  # Ask user for library section
    shelf = simpledialog.askstring("Add Book", "Shelf")      # Ask user for the shelf number

    if title and book_id and author and year and subject and section and shelf:  # If all info is provided:
        file = open("books.txt", "a")                                           # Open the books file in 'append' mode to add to the end

        file.seek(0, 2)  # Go to the very end of the file
        if file.tell() != 0:  # If the file isn't empty:
            file.write("\n")  # Add a new line first so we don't glue data together

        file.write(  # Write all the gathered info separated by commas
            title + "," +
            book_id + "," +
            author + "," +
            year + "," +
            subject + ",Available," +  # Set the status to "Available" by default
            section + "," +
            shelf
        )

        file.close()  # Close the file
        messagebox.showinfo("Success", "Book added successfully")  # Tell the user it worked


# ===================== SEARCH & LOCATE =====================

def search_by_title(books, title):  # Function to find a book using its name
    for book in books:  # Check every book in the list
        if book[0].lower() == title.lower():  # If the names match (ignoring capital letters):
            return ",".join(book)  # Return the book's information
    return "Book not found"  # If we checked everything and found nothing


def search_by_subject(books, subject):  # Function to find all books in a specific category
    result = []  # Start an empty list for the matches
    for book in books:  # Check every book
        if book[4].lower() == subject.lower():  # If the category matches:
            result.append(",".join(book))  # Add this book to our result list
    return "\n".join(result) if result else "No books found"  # Return list or error message


def books_in_section(books, section):  # Function to find all books in a library section
    result = []  # List to hold the books we find
    for book in books:  # Check every book
        if book[6].lower() == section.lower():  # If the section matches:
            result.append(",".join(book))  # Add to results
    return "\n".join(result) if result else "No books found"


def books_in_shelf(books, shelf):  # Function to find all books on a specific shelf
    result = []  # List to hold the books we find
    for book in books:  # Check every book
        if book[7] == shelf:  # If the shelf number matches:
            result.append(",".join(book))  # Add to results
    return "\n".join(result) if result else "No books found"


def locate_book_by_id(books, book_id):  # Function to find where a specific ID is physically located
    for book in books:  # Check every book
        if book[1] == book_id:  # If the ID matches:
            return "Section: " + book[6] + ", Shelf: " + book[7]  # Tell user where it is
    return "Book not found"


def gui_search():  # Function to show the search menu to the user
    choice = simpledialog.askstring(  # Ask user how they want to search
        "Search / Locate",
        "1- By Title\n"
        "2- By Subject\n"
        "3- By Section\n"
        "4- By Shelf\n"
        "5- Locate by ID"
    )

    if not choice:  # If the user clicks cancel:
        return  # Stop and go back

    value = simpledialog.askstring("Search", "Enter value")  # Ask what specifically they are looking for
    if not value:  # If they enter nothing:
        return  # Stop and go back

    books = load_books("books.txt")  # Load current book data from the file

    if choice == "1":  # If they chose title search:
        result = search_by_title(books, value)
    elif choice == "2":  # If they chose subject search:
        result = search_by_subject(books, value)
    elif choice == "3":  # If they chose section search:
        result = books_in_section(books, value)
    elif choice == "4":  # If they chose shelf search:
        result = books_in_shelf(books, value)
    elif choice == "5":  # If they chose ID location:
        result = locate_book_by_id(books, value)
    else:
        result = "Invalid choice"  # If they typed something else

    messagebox.showinfo("Result", result)  # Show the search result in a popup window


# ===================== SHOW =====================

def gui_show():  # Function to show lists of books
    choice = simpledialog.askstring(  # Ask user what they want to see
        "Show",
        "1- Show All Books\n2- Show Borrowed Books"
    )

    if choice == "1":  # If they want to see everything:
        show_all_books()
    elif choice == "2":  # If they only want borrowed books:
        show_borrowed_books()
    else:
        messagebox.showinfo("Info", "Invalid choice")


def show_all_books():  # Function to display the entire library in a table
    df = pd.read_csv(  # Use pandas to read the text file as a table
        "books.txt",
        header=None,  # The file has no column names at the top
        names=["Title", "ID", "Author", "Year", "Subject", "Status", "Section", "Shelf"]  # Label columns
    )
    messagebox.showinfo("All Books", df.to_string())  # Show the table as text in a popup


def show_borrowed_books():  # Function to show who has what book
    books = load_books("books.txt")  # Get the list of books
    records = load_books("borrow_records.txt")  # Get the list of who borrowed what

    text = ""  # Create an empty string to build the list
    for r in records:  # For every record in the borrow file:
        for b in books:  # Compare it against every book in the library:
            if b[1] == r[1]:  # if the IDs match:
                text += "User ID: " + r[0] + "\n"  # Add the user's name/ID to our text
                text += "Book: " + b[0] + "\n\n"  # Add the book title

    messagebox.showinfo("Borrowed Books", text if text else "No borrowed books")  # Show the list


# ===================== BORROW / RETURN =====================

def borrow_book(record_file, book_file, books, user_id, book_id, borrow_date, due_date):
    records = load_books(record_file)  # Get existing borrowing records

    count = 0  # Start a counter
    for r in records:  # Look at all records
        if r[0] == user_id:  # If the user is found:
            count = count + 1  # Add to their count of borrowed books

    if count >= 2:  # If they already have 3 books:
        return "Borrow limit reached"  # Don't let them take more

    for book in books:  # Look for the book they want
        if book[1] == book_id and book[5] == "Available":  # If it's the right ID and is in the library:
            book[5] = "Borrowed"  # Change its status to "Borrowed"
            edit_books(book_file, books)  # Save this change to the books file

            file = open(record_file, "a")  # Open the records file to add the new borrow
            file.write(user_id + "," + book_id + "," + borrow_date + "," + due_date + "\n")
            file.close()  # Close the file

            return "Book borrowed successfully"

    return "Book not available"  # If the book was already out or ID was wrong


def gui_borrow_book():  # Function to gather info for borrowing a book
    user_id = simpledialog.askstring("Borrow Book", "User ID")
    book_id = simpledialog.askstring("Borrow Book", "Book ID")
    borrow_date = simpledialog.askstring("Borrow Book", "Borrow Date")
    due_date = simpledialog.askstring("Borrow Book", "Due Date")

    if not user_id or not book_id or not borrow_date or not due_date:  # Check if user filled everything
        return

    books = load_books("books.txt")  # Load the library data
    result = borrow_book(  # Run the borrowing logic
        "borrow_records.txt",
        "books.txt",
        books,
        user_id,
        book_id,
        borrow_date,
        due_date
    )

    messagebox.showinfo("Borrow", result)  # Show if it was successful or failed


def return_book(record_file, book_file, books, book_id):  # Function to bring a book back
    records = load_books(record_file)  # Get the list of currently borrowed books

    for book in books:  # Find the book in our main list
        if book[1] == book_id:  # When the ID matches:
            book[5] = "Available"  # Set it back to "Available"
            edit_books(book_file, books)  # Save the update to the books file

            new_records = []  # Create a list to hold the remaining borrow records
            for r in records:  # Look at all current borrows
                if r[1] != book_id:  # If the record is NOT the one we are returning:
                    new_records.append(r)  # Keep it in our list

            edit_books(record_file, new_records)  # Save the new list (removes the returned book)
            return "Book returned successfully"

    return "Book not found"  # If the ID didn't exist in our records


def gui_return_book():  # Function to ask for the ID of the book being returned
    book_id = simpledialog.askstring("Return Book", "Book ID")
    if not book_id:  # If they click cancel:
        return

    books = load_books("books.txt")  # Load data
    result = return_book("borrow_records.txt", "books.txt", books, book_id)  # Process return

    messagebox.showinfo("Return", result)  # Tell the user what happened


# ===================== UPDATE / REMOVE =====================

def gui_remove_book():  # Function to delete a book from the library
    book_id = simpledialog.askstring("Remove Book", "Enter Book ID")
    if not book_id:  # If they click cancel:
        return

    books = load_books("books.txt")  # Load current books
    new_books = []  # List to hold everything except the deleted book

    for book in books:  # Loop through all books
        if book[1] != book_id:  # If it's NOT the book we want to delete:
            new_books.append(book)  # Keep it

    edit_books("books.txt", new_books)  # Save the list (effectively removing the one book)
    messagebox.showinfo("Remove Book", "Book removed successfully")


def gui_update_book():  # Function to change details of an existing book
    book_id = simpledialog.askstring("Update Book", "Enter Book ID")
    if not book_id:  # If cancel:
        return

    books = load_books("books.txt")  # Load data

    for book in books:  # Look for the book to change
        if book[1] == book_id:  # If found:
            # Ask for new info; if user leaves it blank, it keeps the old info
            new_title = simpledialog.askstring("Update Book", "New Title (" + book[0] + ")")
            if new_title:
                book[0] = new_title

            new_author = simpledialog.askstring("Update Book", "New Author (" + book[2] + ")")
            if new_author:
                book[2] = new_author

            new_year = simpledialog.askstring("Update Book", "New Year (" + book[3] + ")")
            if new_year:
                book[3] = new_year

            new_subject = simpledialog.askstring("Update Book", "New Subject (" + book[4] + ")")
            if new_subject:
                book[4] = new_subject

            new_section = simpledialog.askstring("Update Book", "New Section (" + book[6] + ")")
            if new_section:
                book[6] = new_section

            new_shelf = simpledialog.askstring("Update Book", "New Shelf (" + book[7] + ")")
            if new_shelf:
                book[7] = new_shelf

            edit_books("books.txt", books)  # Save all the updates
            messagebox.showinfo("Update Book", "Book updated successfully")
            return

    messagebox.showinfo("Update Book", "Book not found")


# ===================== STATISTICS =====================

def gui_statistics():  # Function to choose which graph to view
    choice = simpledialog.askstring(  # Ask user how to group the data
        "Statistics",
        "1- By Subject\n2- By Section\n3- By Shelf"
    )

    books = load_books("books.txt")  # Load data

    if choice == "1":  # Show subject graph
        statistics_by_subject(books)
    elif choice == "2":  # Show section graph
        statistics_by_section(books)
    elif choice == "3":  # Show shelf graph
        statistics_by_shelf(books)
    else:
        messagebox.showinfo("Info", "Invalid choice")


def statistics_by_subject(books):  # Logic to count books by category and draw a bar chart
    data = {}  # Dictionary to store counts (e.g., {'Math': 5})
    for book in books:  # Loop through all books
        data[book[4]] = data.get(book[4], 0) + 1  # Add 1 to the count for this subject
    plt.bar(data.keys(), data.values())  # Create the bar chart
    plt.title("Books per Subject")  # Set graph title
    plt.show()  # Pop up the graph window


def statistics_by_section(books):  # Logic to count books per section and draw graph
    data = {}
    for book in books:
        data[book[6]] = data.get(book[6], 0) + 1
    plt.bar(data.keys(), data.values())
    plt.title("Books per Section")
    plt.show()


def statistics_by_shelf(books):  # Logic to count books per shelf and draw graph
    data = {}
    for book in books:
        data[book[7]] = data.get(book[7], 0) + 1
    plt.bar(data.keys(), data.values())
    plt.title("Books per Shelf")
    plt.show()


# ===================== MAIN GUI =====================

def start_gui():  # Function to build the main application window
    window = tk.Tk()  # Create the main window container
    window.title("Library Management System")  # Set window title
    window.geometry("420x700")  # Set the size of the window

    tk.Label(window, text="LIBRARY MENU", font=("Arial", 18, "bold")).pack(pady=20)  # Main title text

    def btn(text, cmd):  # Helper to quickly make buttons
        tk.Button(window, text=text, width=32, height=2, command=cmd).pack(pady=4)

    # List of buttons and the functions they trigger when clicked:
    btn("Add Book", gui_add_book)
    btn("Search / Locate", gui_search)
    btn("Show", gui_show)
    btn("Borrow Book", gui_borrow_book)
    btn("Return Book", gui_return_book)
    btn("Update Book", gui_update_book)
    btn("Remove Book", gui_remove_book)
    btn("Statistics", gui_statistics)
    btn("Exit", window.destroy)  # Button to close the program

    window.mainloop()  # Keep the window open and running


# ===================== START PROGRAM =====================

start_gui()  # This line actually runs the code