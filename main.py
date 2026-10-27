from library import Library
from book import Book
from user import User

def run():
    lib = Library()
    lib.add_book(Book("1984", "George Orwell", 1949, "ISBN001"))
    lib.add_book(Book("To Kill a Mockingbird", "Harper Lee", 1960, "ISBN002"))
    lib.add_book(Book("The Great Gatsby", "F. Scott Fitzgerald", 1925, "ISBN003"))
    lib.add_book(Book("Moby Dick", "Herman Melville", 1851, "ISBN004"))
    lib.add_book(Book("Pride and Prejudice", "Jane Austen", 1813, "ISBN005"))
    lib.add_book(Book("War and Peace", "Leo Tolstoy", 1869, "ISBN006"))

    lib.add_user(User("Anna", "U001"))
    lib.add_user(User("Juan", "U002"))
    lib.add_user(User("Mary", "U003"))
    lib.add_user(User("Jaciel", "U004"))

    while True:
        print("\n--- Library System ---")
        print("1. Borrow a book")
        print("2. Return a book")
        print("3. View user history")
        print("0. Exit")

        option = input("Choose an option: ")

        if option == "0":
            break
        elif option == "2":
            isbn = input("Enter book ISBN: ")
            user_id = input("Enter user ID: ")
            try:
                lib.borrow_book(user_id, isbn)
                print("Book successfully borrowed")
            except ValueError as e:
                print("Error:", e)
        elif option == "1":
            isbn = input("Enter book ISBN: ")
            user_id = input("Enter user ID: ")
            try:
                lib.return_book(user_id, isbn)
                print("Book successfully returned")
            except ValueError as e:
                print("Error:", e)
        elif option == "3":
            user_id = input("Enter user ID: ")
            try:
                user = lib._find_user(user_id)
                print("User history:", user.get_history())
            except ValueError as e:
                print("Error:", e)
        else:
            print("Invalid option")

if __name__ == "__main__":
    run()
