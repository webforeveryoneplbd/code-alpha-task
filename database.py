import sqlite3

# Fonction de recherche de livres par titre ou auteur
def search_books(query):
    # Connexion à la base de données
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    
    # Requête pour rechercher des livres
    cursor.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?", ('%' + query + '%', '%' + query + '%'))
    books = cursor.fetchall()
    
    # Fermeture de la connexion
    conn.close()
    
    # Retour des résultats de la recherche
    return books

# Classe pour gérer la base de données
class Database:
    def __init__(self, db_name):
        # Connexion à la base de données
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, columns):
        # Création de la table avec les colonnes spécifiées
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ("
        for column in columns:
            query += f"{column[0]} {column[1]}, "
        query = query[:-2] + ")"
        self.cursor.execute(query)
        self.conn.commit()

    def insert_data(self, table_name, data):
        # Insertion des données dans la table
        query = f"INSERT INTO {table_name} VALUES ("
        for _ in data:
            query += "?, "
        query = query[:-2] + ")"
        self.cursor.execute(query, data)
        self.conn.commit()

    def select_data(self, table_name, conditions=None):
        # Sélection des données de la table avec des conditions facultatives
        query = f"SELECT * FROM {table_name}"
        if conditions:
            query += " WHERE "
            for condition in conditions:
                query += f"{condition[0]} {condition[1]} ?, "
            query = query[:-2]
        self.cursor.execute(query, [condition[2] for condition in conditions] if conditions else [])
        return self.cursor.fetchall()

    def update_data(self, table_name, data, conditions):
        # Mise à jour des données dans la table avec des conditions
        query = f"UPDATE {table_name} SET "
        for column, value in data.items():
            query += f"{column} = ?, "
        query = query[:-2] + " WHERE "
        for condition in conditions:
            query += f"{condition[0]} {condition[1]} ?, "
        query = query[:-2]
        self.cursor.execute(query, list(data.values()) + [condition[2] for condition in conditions])
        self.conn.commit()

    def delete_data(self, table_name, conditions):
        # Suppression des données de la table avec des conditions
        query = f"DELETE FROM {table_name} WHERE "
        for condition in conditions:
            query += f"{condition[0]} {condition[1]} ?, "
        query = query[:-2]
        self.cursor.execute(query, [condition[2] for condition in conditions])
        self.conn.commit()

    def close_connection(self):
        # Fermeture de la connexion à la base de données
        self.conn.close()

# Exemple d'utilisation
if __name__ == "__main__":
    db = Database('books.db')

    # Création des tables
    db.create_table('categories', [('id', 'INTEGER PRIMARY KEY'), ('name', 'TEXT NOT NULL')])
    db.create_table('books', [('id', 'INTEGER PRIMARY KEY'), ('title', 'TEXT NOT NULL'), ('author', 'TEXT NOT NULL'), ('isbn', 'TEXT NOT NULL'), ('category', 'TEXT NOT NULL')])
    db.create_table('borrowings', [('id', 'INTEGER PRIMARY KEY'), ('book_id', 'INTEGER NOT NULL'), ('borrow_date', 'DATE NOT NULL'), ('due_date', 'DATE NOT NULL')])

    # Insertion de données
    db.insert_data('categories', (1, 'Fiction'))
    db.insert_data('books', (1, 'Book Title', 'Author Name', 'ISBN Number', 'Fiction'))
    db.insert_data('borrowings', (1, 1, '2022-01-01', '2022-01-15'))

    # Insertion de données de livres
    db.insert_data('books', (1, 'Le Comte de Monte-Cristo', 'Alexandre Dumas', '978-2-07-041938-5', 'Roman'))
    db.insert_data('books', (2, 'Les Misérables', 'Victor Hugo', '978-2-07-041939-2', 'Roman'))
    db.insert_data('books', (3, 'Pride and Prejudice', 'Jane Austen', '978-1-85-326050-9', 'Roman'))
    db.insert_data('books', (4, 'Le Petit Prince', 'Antoine de Saint-Exupéry', '978-2-07-041940-8', 'Roman'))
    db.insert_data('books', (5, 'Harry Potter et la Pierre philosophale', 'J.K. Rowling', '978-2-07-051842-7', 'Fantastique'))

    # Sélection de données
    print(db.select_data('books'))

    # Mise à jour de données
    db.update_data('books', {'title': 'New Book Title'}, [('id', '=', 1)])

    # Suppression de données
    db.delete_data('books', [('id', '=', 1)])

    # Fermeture de la connexion
    db.close_connection()
