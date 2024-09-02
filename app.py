from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import db, Book, BorrowingHistory

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialise db avec l'application Flask
db.init_app(app)

# Créer les tables dans la base de données
with app.app_context():
    db.create_all()

@app.route('/api/book/<int:id>')
def api_book_details(id):
    book = Book.query.get(id)
    if book:
        return jsonify({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'genre': book.category,
            'status': book.status
        })
    return jsonify({'error': 'Livre non trouvé'}), 404

@app.route('/borrow/<int:book_id>', methods=['POST'])
def api_borrow_book(book_id):
    book = Book.query.get(book_id)
    if book and book.status == 'Available':
        book.status = 'Borrowed'
        db.session.commit()
        return jsonify({'success': True, 'message': 'Livre emprunté avec succès'})
    return jsonify({'success': False, 'message': 'Livre non disponible ou n\'existe pas'}), 400

@app.route('/')
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)

@app.route('/search', methods=['POST'])
def search():
    search_term = request.form.get('search', '')
    print(f"Search term: {search_term}")  # Debug: print search term
    books = Book.query.filter(Book.title.contains(search_term)).all()
    print(f"Found books: {books}")  # Debug: print found books
    return render_template('index.html', books=books)


@app.route('/book/<int:id>')
def book_details(id):
    book = Book.query.get(id)
    return render_template('book_liste.html', book=book)

@app.route('/borrow/<int:book_id>')
def borrow_book(book_id):
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
