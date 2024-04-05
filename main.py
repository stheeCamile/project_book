from flask import Flask, request, jsonify, render_template, redirect, url_for
from controllers.book_controller import insert_book, search_book
from controllers.user_controller import login
from services.auth_service import verificar_token  

app = Flask(__name__)

# Rota de login
@app.route("/login", methods=["GET", "POST"])
def login_route():
    if request.method == "POST":
        response = login()
        if response[1] == 200:
            return redirect(url_for('insert_book_route'))
        else:
            return response[0]
    else:
        return render_template("login.html")

# Rota de inserção de livro

@app.route("/insert_book", methods=["GET", "POST"])
def insert_book_route():
    if request.method == "POST":
        token = request.headers.get('Authorization')
 
        usuario = verificar_token(token)
        if not usuario:
            return jsonify({'mensagem': 'Token de autenticação inválido'}), 401

        name = request.form.get("name")
        release_date = request.form.get("release_date")
        isbn = request.form.get("isbn")
        author = request.form.get("author")

        if not name or not release_date or not isbn or not author:
            return jsonify({'mensagem': 'Por favor, preencha todos os campos'}), 400

        insert_book(name, release_date, isbn, author)

        # Redirecionar para a rota de busca de livro após adicionar com sucesso
        return redirect(url_for('search_book_route'))

    else:
        return render_template("insert_book.html")

# Rota de busca de livro
@app.route("/search_book", methods=["GET", "POST"])
def search_book_route():
    if request.method == "POST":
        token = request.headers.get('Authorization')
 
        usuario = verificar_token(token)
        if not usuario:
            return jsonify({'mensagem': 'Token de autenticação inválido'}), 401
        name = request.form.get("name")
        books = search_book(name)
        serialized_books = [book.to_dict() for book in books] 

        return jsonify(serialized_books)
    else:
        return render_template("search_book.html")

if __name__ == "__main__":
    app.run(debug=True)