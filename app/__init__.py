from flask import Flask
# from .routes.hello_world_routes import hello_world_bp
from .db import db, migrate
from .models import book, author, genre
from .routes.book_routes import bp as books_bp
from app.routes.author_routes import bp as authors_bp
from app.routes.genre_routes import bp as genres_bp
import os



def create_app(config=None):
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

    if config:
        # Merge `config` into the app's configuration
        # to override the app's default settings
        app.config.update(config)
        
    db.init_app(app)
    migrate.init_app(app, db)

    # # Register Blueprints here
    # app.register_blueprint(hello_world_bp)

    # Registering Blueprint
    app.register_blueprint(books_bp)
    app.register_blueprint(authors_bp)
    app.register_blueprint(genres_bp)

    return app