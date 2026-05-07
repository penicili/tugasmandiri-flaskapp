from flask import Blueprint, jsonify, request
from app import db as database
from app import cache
from app.models import Book

bp = Blueprint('books', __name__)


@bp.get('/')
def health_check():
    return 'OK', 200


@bp.get('/books')
@bp.get('/books/<int:book_id>')
def get_book(book_id: int | None = None):
    cache_key = f'book:{book_id}' if book_id is not None else 'books:all'

    cached = cache.cache_get(cache_key)
    if cached is not None:
        return jsonify(cached), 200

    client = database.get_db()
    if book_id is not None:
        res = client.table('books').select('*').eq('id', book_id).execute()
        if not res.data:
            return '', 404
        result = res.data[0]
    else:
        res = client.table('books').select('*').execute()
        result = res.data

    cache.cache_set(cache_key, result)
    return jsonify(result), 200


@bp.post('/books')
def add_book():
    data = request.get_json()
    if not data or not all(k in data for k in ('title', 'author', 'published_year')):
        return '', 400
    client = database.get_db()
    res = client.table('books').insert({
        'title': data['title'],
        'author': data['author'],
        'published_year': data['published_year'],
    }).execute()
    if not res.data:
        return '', 400
    cache.cache_delete('books:all')
    return jsonify(res.data[0]), 201


@bp.put('/books/<int:book_id>')
def update_book(book_id: int):
    data = request.get_json()
    if not data or not all(k in data for k in ('title', 'author', 'published_year')):
        return '', 400
    client = database.get_db()
    res = client.table('books').update({
        'title': data['title'],
        'author': data['author'],
        'published_year': data['published_year'],
    }).eq('id', book_id).execute()
    if not res.data:
        return '', 404
    cache.cache_delete(f'book:{book_id}', 'books:all')
    return jsonify(res.data[0]), 200


@bp.delete('/books/<int:book_id>')
def delete_book(book_id: int):
    client = database.get_db()
    res = client.table('books').delete().eq('id', book_id).execute()
    if not res.data:
        return '', 404
    cache.cache_delete(f'book:{book_id}', 'books:all')
    return jsonify({'message': f'Book {book_id} deleted successfully'}), 200
