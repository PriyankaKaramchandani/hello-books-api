from flask import Blueprint, make_response, abort, request, Response
from app.models.book import Book
from app.models.author import Author
from ..db import db
from app.routes.route_utilities import validate_model, create_model

# Creating an instance of Blueprint
bp = Blueprint("books", __name__, url_prefix="/books")

@bp.post("")
def create_book():
    request_body = request.get_json()
    return create_model(Book, request_body)

# @bp.post("")
# def create_book():
#     request_body = request.get_json()

#     try:
#         new_book = Book.from_dict(request_body)

#     except KeyError as error:
#         response = {"message": f"Invalid request: missing {error.args[0]}"}
#         abort(make_response(response, 400))
    
#     db.session.add(new_book)
#     db.session.commit()

#     response = new_book.to_dict()

#     return response, 201

@bp.get("")
def get_all_books():

    query = db.select(Book)

    title_param = request.args.get("title") 
    if title_param:
        query = query.where(Book.title.ilike(f"%{title_param}%"))
    description_param = request.args.get("description")
    if description_param:
        query = query.where(Book.title.ilike(f"%{description_param}%"))
    
    query = query.order_by(Book.id)
    books = db.session.scalars(query)
    
    books_response = []
    for book in books:
        books_response.append(
            book.to_dict()
        )
    return books_response

@bp.get("/<book_id>")
def get_one_book(book_id):
    book = validate_model(Book, book_id)

    return book.to_dict()

@bp.put("/<book_id>")
def update_one_book(book_id):
    book = validate_model(Book, book_id)
    request_body = request.get_json()

    book.title = request_body["title"]
    book.description = request_body["description"]

    if "author_id" in request_body:
        book.author_id = request_body["author_id"]  # Update the author_id with the new author_id
    elif "author" in request_body:
        author_data = request_body["author"]
        author = Author.from_dict(author_data)  # Create a new Author instance from provided data
        book.author = author

    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.delete("/<book_id>")
def delete_book(book_id):
    book = validate_model(Book, book_id)
    db.session.delete(book)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

# def validate_book(book_id):
#     try:
#         input_id = int(book_id)
#     except:
#         response = {"message": f"book {book_id} invalid"}
#         abort(make_response(response , 400))
    
#     query = db.select(Book).where(Book.id == book_id)
#     book = db.session.scalar(query)

#     if not book:
#         response = make_response({"message": f"Book {book_id} is not found"}, 404) # make_response() can take key-value pairs like seen here or even string message
#         abort(response) # abort() can only take response object or status code. It cannot take message like string or dict directly.
#     return book
    
