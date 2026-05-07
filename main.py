from flask import Flask, jsonify, request
import sqlite3
import os
import controller
import dotenv
import waitress
import logging

dotenv.load_dotenv()

app = Flask(__name__)
DB = os.getenv('DB_DATABASE', 'app.db')

@app.route('/')
def health_check():
    return 'OK', 200

@app.route('/books', methods=['GET'])
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id: int | None = None):
    result = controller.get_book(book_id)
    if result is None:
        return '', 404
    if isinstance(result, controller.Book):
        result = result.to_dict()
    elif isinstance(result, list):
        result = [book.to_dict() if isinstance(book, controller.Book) else book for book in result]
    return jsonify(result), 200

@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    if not all(key in data for key in ('title', 'author', 'published_year')):
        return '', 400
    create_book = controller.add_book(book_data=controller.Book.from_dict(data))
    if create_book is None:
        return '', 400
    if isinstance(create_book, controller.Book):
        create_book = create_book.to_dict()
    return jsonify(create_book), 201

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id: int):
    data = request.get_json()
    if not all(key in data for key in ('title', 'author', 'published_year')):
        return '', 400
    updated_book = controller.update_book(id=book_id, book_data=controller.Book.from_dict(data))
    if updated_book is None:
        return '', 404
    if isinstance(updated_book, controller.Book):
        updated_book = updated_book.to_dict()
    return jsonify(updated_book), 200

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id: int):
    deleted = controller.delete_book(book_id)
    if not deleted:
        return '', 404
    return jsonify({'message': f'Book {book_id} deleted successfully'}), 200


def init_db():
    try:
        print(f"Attempting to connect to the database at {DB}...")
        db = sqlite3.connect(DB)
        cursor = db.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT, author TEXT, published_year INTEGER)')
        db.commit()
        db.close()
        print("Database initialized successfully.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")

if __name__ == '__main__':
    # connect to db
    init_db()   
    
    logging.basicConfig(level=logging.DEBUG)
    
    waitress.serve(app, host='0.0.0.0', port=5000)
