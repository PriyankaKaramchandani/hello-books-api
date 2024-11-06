from flask import Blueprint, make_response, abort, request, Response
from app.models.author import Author
from ..db import db
from .route_utilities import create_model, validate_model

bp = Blueprint("authors", __name__, url_prefix="/authors")

@bp.post("")
def create_author():
    request_body = request.get_json()
    return create_model(Author, request_body)

# @bp.get("")
# def get_all_authors():
#     query = db.select(Author)

#     name_param = request.args.get("name")
#     if name_param:
#         query = query.where(Author.name.ilike(f"%{name_param}%"))

#     query = query.order_by(Author.id)
#     authors = db.session.scalars(query)

#     authors_response = [author.to_dict() for author in authors]

#     return authors_response

@bp.post("/<author_id>/books")
def create_book_with_author(author_id):
    author = validate_model(Author, author_id)
    
    request_body = request.get_json()
    request_body["author_id"] = author.id
    return create_model(Book, request_body)

@bp.get("/<author_id>/books")
def get_books_by_author(author_id):
    author = validate_model(Author, author_id)
    response = [book.to_dict() for book in author.books]
    return response

# @bp.post("")
# def create_author():
#     request_body = request.get_json()

#     try:
#         new_author = Author.from_dict(request_body)
        
#     except KeyError as error:
#         response = {"message": f"Invalid request: missing {error.args[0]}"}
#         abort(make_response(response, 400))
    
#     db.session.add(new_author)
#     db.session.commit()

#     return make_response(new_author.to_dict(), 201)

# @bp.post("/<author_id>/books")
# def create_book_with_author(author_id):
#     author = validate_model(Author, author_id)
    
#     request_body = request.get_json()
#     request_body["author_id"] = author.id

#     try:
#         new_book = Book.from_dict(request_body)

#     except KeyError as error:
#         response = {"message": f"Invalid request: missing {error.args[0]}"}
#         abort(make_response(response, 400))
        
#     db.session.add(new_book)
#     db.session.commit()

#     return make_response(new_book.to_dict(), 201)
