from . import book_blueprint as book_bp
from flask import request
from flask_jwt_extended import jwt_required, current_user
from ..models import Book  
from ..utils import bad_request_if_none

@book_bp.route("/new", methods=["POST"])
@jwt_required()
def handle_create_book():
    data = request.json

    if data is None:
        response = {"message": "Invalid request"}
        return response, 400

    title = data.get("title")
    if title is None or title == "":
        response = {"message": "Title is required"}
        return response, 400

    author = data.get("author")

    new_book = Book(title=title, author=author, user_id=current_user.id)
    new_book.create()

    response = {"message": "Book created", "book": new_book.to_response()}
    return response, 201

@book_bp.route("/all", methods=["GET"])
@jwt_required()
def handle_get_all_books():
    books = Book.query.all()
    response = {"message": "Books retrieved", "books": [book.to_response() for book in books]}
    return response, 200

@book_bp.route("/mine", methods=["GET"])
@jwt_required()
def handle_get_my_books():
    books = Book.query.filter_by(user_id=current_user.id).all()
    response = {"message": "Your books", "books": [book.to_response() for book in books]}
    return response, 200

@book_bp.route("/<int:book_id>", methods=["GET"])
@jwt_required()
def handle_get_one_book(book_id):
    book = Book.query.get(book_id)
    if book is None:
        response = {"message": "Book not found"}
        return response, 404

    response = {"message": "Book found", "book": book.to_response()}
    return response, 200

@book_bp.route("/delete-book/<int:book_id>", methods=["DELETE"])
@jwt_required()
def handle_delete_book(book_id):
    book = Book.query.get(book_id)
    if book is None:
        response = {"message": "Book not found"}
        return response, 404

    if book.user_id != current_user.id:
        response = {"message": "Unauthorized - This book does not belong to you."}
        return response, 401

    book.delete()
    response = {"message": "Book deleted"}
    return response, 204

@book_bp.route("/update-book/<int:book_id>", methods=["PUT"])
@jwt_required()
def handle_update_book(book_id):
    book = Book.query.get(book_id)
    if book is None:
        response = {"message": "Book not found"}
        return response, 404

    if book.user_id != current_user.id:
        response = {"message": "Unauthorized - This book does not belong to you."}
        return response, 401

    data = request.json
    title = data.get("title", book.title)
    author = data.get("author", book.author)

    book.title = title
    book.author = author
    book.update()

    response = {"message": "Book updated", "book": book.to_response()}
    return response, 200