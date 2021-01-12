from library import app, db
from models import *

from flask import jsonify, request


@app.route("/books", methods=["GET"])
def get_books():
    books = Book.query.all()
    entities = request.args.get("allEntities", False)
    ret = [a.to_json(entities) for a in books]
    return jsonify(ret)


@app.route("/books/<book_id>", methods=["GET"])
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    entities = request.args.get("allEntities", False)
    ret = book.to_json(entities)
    return jsonify(ret)


@app.route("/books", methods=["POST"])
def create_books():
    book = Book(name=request.form["name"])
    db.session.add(book)
    db.session.commit()
    ret = book.to_json()
    return jsonify(ret)


@app.route("/books/<book_id>/authors", methods=["POST"])
def add_book_to_book(book_id):
    book = Book.query.get_or_404(book_id)
    author = Author.query.filter_by(name=request.form["name"]).first()
    if author is None:
        author = Author(name=request.form["name"])
        book.authors.append(author)
        db.session.add(author)
        db.session.add(book)
        db.session.commit()
    ret = book.to_json(entities=True)
    return jsonify(ret)


@app.route("/books/<book_id>", methods=["PUT"])
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    book.title = request.form["title"]
    db.session.add(book)
    db.session.commit()
    entities = request.args.get("allEntities", False)
    ret = book.to_json(entities)
    return jsonify(ret)


@app.route("/books/<book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return jsonify("")

