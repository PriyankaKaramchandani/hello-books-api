from flask import Blueprint, request
from app.models.genre import Genre
from app.routes.route_utilities import create_model, get_models_with_filters

bp = Blueprint("genres", __name__, url_prefix="/genres")

bp.get("")
def get_all_genres():
    return get_models_with_filters(Genre, request.args)

bp.post("")
def create_one_genre():
    request_body = request.get_json()
    return create_model(Genre, request_body)

@bp.post("/<genre_id>/books")
def create_book_with_genre(genre_id):
    genre = validate_model(Genre, genre_id)

    request_body = request.get_json()
    request_body["genres"] = [genre]
    return create_model(Book, request_body)

@bp.get("/,genre_id>/books")
def get_books_with_genre(genre_id):
    genre = validate_model(Genre, genre_id)
    response = [book.to_dict() for book in genre.books]
    return response