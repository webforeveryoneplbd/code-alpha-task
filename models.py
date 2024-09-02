from flask_sqlalchemy import SQLAlchemy

# Initialise l'instance de base de données
db = SQLAlchemy()

# Modèle de table pour Book
class Book(db.Model):
    __tablename__ = 'books'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    isbn = db.Column(db.String, nullable=False, unique=True)
    category = db.Column(db.String, nullable=False)
    status = db.Column(db.String, default='Available')

# Modèle de table pour Borrower
class Borrower(db.Model):
    __tablename__ = 'borrowers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

# Modèle de table pour BorrowingHistory
class BorrowingHistory(db.Model):
    __tablename__ = 'borrowing_history'
    
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    borrower_id = db.Column(db.Integer, db.ForeignKey('borrowers.id'), nullable=False)
    borrow_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=True)

def load_initial_data():
    # Livres à ajouter
    new_books = [
        {'title': 'Le Comte de Monte-Cristo', 'author': 'Alexandre Dumas', 'isbn': '978-2-07-041938-5', 'category': 'Roman'},
        {'title': 'Les Misérables', 'author': 'Victor Hugo', 'isbn': '978-2-07-041939-2', 'category': 'Roman'},
        # Ajoutez plus de livres ici...
    ]

    for book_data in new_books:
        # Vérifiez si le livre existe déjà
        existing_book = Book.query.filter_by(isbn=book_data['isbn']).first()
        if not existing_book:
            # Ajouter le livre s'il n'existe pas encore
            new_book = Book(
                title=book_data['title'],
                author=book_data['author'],
                isbn=book_data['isbn'],
                category=book_data['category'],
                status='Available'
            )
            db.session.add(new_book)
    
    db.session.commit()

