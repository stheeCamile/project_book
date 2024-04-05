import mysql.connector
from config.config import db_config
from Model.book_model import Book
from flask import jsonify
from datetime import datetime


conn = mysql.connector.connect(**db_config)

def add_book(name, release_date, isbn, author):
    cursor = conn.cursor()
    release_date_str = release_date
    release_date = datetime.strptime(release_date_str, '%d%m%Y').date()

    cursor.execute("INSERT INTO books (name, release_date, isbn, author) VALUES (%s, %s, %s, %s)", (name, release_date, isbn, author))
    conn.commit()
    cursor.close()

def search_book_name(name):
    cursor = conn.cursor()


    cursor.execute("SELECT * FROM books WHERE name LIKE %s", ('%' + name + '%',))

    books_found = cursor.fetchall()

    cursor.close()

    books = []
    for book_data in books_found:
        book_dict = {
            'name': book_data[1],
            'release_date': book_data[2],
            'isbn': book_data[3],
            'author': book_data[4]
        }
        try:
            book = Book(**book_dict)  
            books.append(book)
            print("Livro adicionado:", book_data)
        except TypeError as e:
            print("Erro ao criar livro:", e)
            print("Dados inválidos:", book_data)

    print("Livros encontrados:", books)
    return books 

