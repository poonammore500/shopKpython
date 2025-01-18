from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

class Book:
    def __init__(self, title, author, price, stock):
        self.title = title
        self.author = author
        self.price = price
        self.stock = stock

    def __str__(self):
        return f"{self.title} by {self.author} - ${self.price} ({self.stock} in stock)"

class Bookstore:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def get_books(self):
        return self.books

    def search_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None

    def purchase_book(self, title, quantity):
        book = self.search_book(title)
        if book:
            if book.stock >= quantity:
                book.stock -= quantity
                return True
        return False

store = Bookstore()
store.add_book(Book("1984", "George Orwell", 10.99, 5))
store.add_book(Book("To Kill a Mockingbird", "Harper Lee", 8.99, 2))

@app.route('/')
def home():
    return render_template('index.html', books=store.get_books())

@app.route('/purchase', methods=['POST'])
def purchase():
    title = request.form.get('title')
    quantity = int(request.form.get('quantity'))
    if store.purchase_book(title, quantity):
        return redirect(url_for('home'))
    return "Book not available or insufficient stock", 400

if __name__ == "__main__":
    app.run(debug=True)
