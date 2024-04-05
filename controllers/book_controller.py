from services.book_service import add_book, search_book_name
from flask import jsonify

def insert_book(name, release_date, isbn, author):
    
    if not name or not release_date or not isbn or not author:
        return jsonify({'mensagem': 'Por favor, preencha todos os campos'}), 400

    add_book(name, release_date, isbn, author)

    return jsonify({'mensagem': 'Livro adicionado com sucesso'}), 200

def search_book(name):
    book_name = name
    book_results = search_book_name(book_name)
    return book_results
