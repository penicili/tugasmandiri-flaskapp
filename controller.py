import sqlite3
import os
db = os.getenv('DB_DATABASE', 'app.db')

class Book: 
    def __init__(self, id: int | None, title: str, author: str, published_year: int):
        self.id = id
        self.title = title
        self.author = author
        self.published_year = published_year

    @classmethod
    def from_row(cls, row: tuple):
        return cls(row[0], row[1], row[2], row[3])

    @classmethod
    def from_dict(cls, book_data: dict):
        return cls(
            book_data.get('id'),
            book_data['title'],
            book_data['author'],
            book_data['published_year'],
        )

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'published_year': self.published_year,
        }

def get_book(id: int | None = None):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    if id is not None:
        cursor.execute('SELECT * FROM books WHERE id = ?', (id,))
        book_row = cursor.fetchone()
        conn.close()
        if book_row:
            return Book.from_row(book_row)
        else:
            return None
    else:
        cursor.execute('SELECT * FROM books')
        books = cursor.fetchall()
        conn.close()
        return [Book.from_row(book) for book in books]
    
    
def add_book(book_data: Book):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO books (title, author, published_year) VALUES (?, ?, ?)',
        (book_data.title, book_data.author, book_data.published_year),
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return get_book(new_id)

def update_book(id: int, book_data: Book):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute('UPDATE books SET title = ?, author = ?, published_year = ? WHERE id = ?', (book_data.title, book_data.author, book_data.published_year, id))
    conn.commit()
    conn.close()
    return get_book(id)

def delete_book(id: int):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM books WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return True