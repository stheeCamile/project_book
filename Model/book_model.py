class Book:
    def __init__(self, name, release_date, isbn, author):
        self.name = name
        self.release_date = release_date
        self.isbn = isbn
        self.author = author

    def to_dict(self):
        return {
            
            'name': self.name,
            'release_date': self.release_date.strftime('%Y-%m-%d'),  
            'isbn': self.isbn,
            'author': self.author
        }