class User:
    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id
        self.history = []

    def register_borrow(self, book):
        self.history.append(f"Borrwed: {book.title}")

    def register_return(self, book):
        self.history.append(f"Reurned: {book.title}")

    def get_history(self):
        return self.history
