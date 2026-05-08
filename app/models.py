class Book:
    # Model untuk buku
    def __init__(self, id: int | None, title: str, author: str, published_year: int):
        self.id = id
        self.title = title
        self.author = author
        self.published_year = published_year
    # Method untuk convert data dari database ke objek Book
    @classmethod
    def from_row(cls, row: tuple):
        return cls(row[0], row[1], row[2], row[3])
    # Convert data dari dict ke objek Book
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            data.get('id'),
            data['title'],
            data['author'],
            data['published_year'],
        )
    # Method untuk convert objek Book ke dictionary, biar bisa disimpan di cache
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'published_year': self.published_year,
        }
