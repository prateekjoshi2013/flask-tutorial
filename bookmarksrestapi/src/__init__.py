from http import HTTPStatus
import os
from flask import Flask,jsonify,redirect
from src.database import Bookmark
from src.auth import auth
from src.bookmarks import bookmarks
from src.database import db
from flask_jwt_extended import JWTManager

def create_app(test_config=None):
    app=Flask(__name__,instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get('SECRET_KEY'),
            SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DB_URI'),
            SQLALCHEMY_TRACK_MODIFICATIONS=os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS'),
            JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY')
        )
    else:
        app.config.from_mapping(test_config)

    db.app=app
    db.init_app(app)

    JWTManager(app)
    
    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)

    @app.get('/<short_url>')
    def redirect_to_url(short_url):
        bookmark=Bookmark.query.filter_by(short_url=short_url).first_or_404()
        if bookmark:
            bookmark.visits=bookmark.visits+1
            db.session.commit()
            return redirect(bookmark.url)

    @app.errorhandler(HTTPStatus.NOT_FOUND.value)
    def handle_404(e):
        return jsonify({"error":"not found"}),HTTPStatus.NOT_FOUND.value

    @app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR.value)
    def handle_500(e):
        return jsonify({"error": "Internal Server Error"}),HTTPStatus.INTERNAL_SERVER_ERROR.value

    return app
