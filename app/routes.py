from flask import Blueprint, jsonify, request
from app import db as database
from app.models import Book

bp = Blueprint('books', __name__)


@bp.get('/')
def health_check():
    return 'OK', 200


@bp.get('/books')
@bp.get('/books/<int:book_id>')
def get_book(book_id: int | None = None):
    conn = database.get_db()
    cursor = conn.cursor()
    if book_id is not None:
        cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
        row = cursor.fetchone()
        conn.close()
        if row is None:
            return '', 404
        return jsonify(Book.from_row(row).to_dict()), 200
    else:
        cursor.execute('SELECT * FROM books')
        rows = cursor.fetchall()
        conn.close()
        return jsonify([Book.from_row(r).to_dict() for r in rows]), 200


@bp.post('/books')
def add_book():
    data = request.get_json()
    if not data or not all(k in data for k in ('title', 'author', 'published_year')):
        return '', 400
    conn = database.get_db()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO books (title, author, published_year) VALUES (?, ?, ?)',
        (data['title'], data['author'], data['published_year']),
    )
    conn.commit()
    new_id = cursor.lastrowid
    cursor.execute('SELECT * FROM books WHERE id = ?', (new_id,))
    row = cursor.fetchone()
    conn.close()
    return jsonify(Book.from_row(row).to_dict()), 201


@bp.put('/books/<int:book_id>')
def update_book(book_id: int):
    data = request.get_json()
    if not data or not all(k in data for k in ('title', 'author', 'published_year')):
        return '', 400
    conn = database.get_db()
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE books SET title = ?, author = ?, published_year = ? WHERE id = ?',
        (data['title'], data['author'], data['published_year'], book_id),
    )
    conn.commit()
    cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        return '', 404
    return jsonify(Book.from_row(row).to_dict()), 200


@bp.delete('/books/<int:book_id>')
def delete_book(book_id: int):
    conn = database.get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM books WHERE id = ?', (book_id,))
    if cursor.fetchone() is None:
        conn.close()
        return '', 404
    cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': f'Book {book_id} deleted successfully'}), 200
