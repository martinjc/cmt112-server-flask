from library import app, db
from models import *

from flask import jsonify, request


@app.route("/books", methods=["GET", "POST"])
def get_books():
    if request.method == "GET":
        books = Book.query.all()
        entities = request.args.get("allEntities", False)
        ret = [a.to_json(entities) for a in books]
        return jsonify(ret)
    elif request.method == "POST":
        book = Book(title=request.json["title"], isbn=request.json["isbn"])
        db.session.add(book)
        db.session.commit()
        ret = book.to_json()
        return jsonify(ret)


@app.route("/books/<book_id>", methods=["GET", "PUT", "DELETE"])
def get_book(book_id):
    if request.method == "GET":
        book = Book.query.get_or_404(book_id)
        entities = request.args.get("allEntities", False)
        ret = book.to_json(entities)
        return jsonify(ret)
    elif request.method == "PUT":
        book = Book.query.get_or_404(book_id)
        book.title = request.json["title"]
        db.session.add(book)
        db.session.commit()
        entities = request.args.get("allEntities", False)
        ret = book.to_json(entities)
        return jsonify(ret)
    elif request.method == "DELETE":
        book = Book.query.get_or_404(book_id)
        db.session.delete(book)
        db.session.commit()
        return jsonify("")


@app.route("/books/<book_id>/authors", methods=["POST"])
def add_author_to_book(book_id):
    book = Book.query.get_or_404(book_id)
    author = Author.query.filter_by(name=request.json["authorName"]).first()
    if author is None:
        author = Author(name=request.json["authorName"])
        book.authors.append(author)
        db.session.add(author)
        db.session.add(book)
        db.session.commit()
    ret = book.to_json(entities=True)
    return jsonify(ret)


@app.route("/books/<book_id>/authors/<author_id>", methods=["POST"])
def add_author_to_book_by_id(book_id):
    book = Book.query.get_or_404(book_id)
    author = Author.query.get_or_404(author_id)
    book.authors.append(author)
    db.session.add(author)
    db.session.add(book)
    db.session.commit()
    ret = book.to_json(entities=True)
    return jsonify(ret)
