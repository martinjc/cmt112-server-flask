from library import app, db
from models import *

from flask import jsonify, request


@app.route("/authors", methods=["GET", "POST"])
def get_authors():
    if request.method == "GET":
        authors = Author.query.all()
        entities = request.args.get("allEntities", False)
        ret = [a.to_json(entities) for a in authors]
        return jsonify(ret)
    elif request.method == "POST":
        author = Author(name=request.json["name"])
        db.session.add(author)
        db.session.commit()
        ret = author.to_json()
        return jsonify(ret)


@app.route("/authors/<author_id>", methods=["GET", "PUT", "DELETE"])
def get_author(author_id):
    if request.method == "GET":
        author = Author.query.get_or_404(author_id)
        entities = request.args.get("allEntities", False)
        ret = author.to_json(entities)
        return jsonify(ret)
    elif request.method == "PUT":
        author = Author.query.get_or_404(author_id)
        author.name = request.json["name"]
        db.session.add(author)
        db.session.commit()
        entities = request.args.get("allEntities", False)
        ret = author.to_json(entities)
        return jsonify(ret)
    elif request.method == "DELETE":
        author = Author.query.get_or_404(author_id)
        db.session.delete(author)
        db.session.commit()
        return jsonify("")


@app.route("/authors/<author_id>/books", methods=["POST"])
def add_book_to_author(author_id):
    author = Author.query.get_or_404(author_id)
    book = Book.query.filter_by(
        title=request.json["bookTitle"], isbn=request.json["bookISBN"]
    ).first()
    if book is None:
        book = Book(title=request.json["bookTitle"], isbn=request.json["bookISBN"])
        author.books.append(book)
        db.session.add(book)
        db.session.add(author)
        db.session.commit()
    ret = author.to_json(entities=True)
    return jsonify(ret)


@app.route("/authors/<author_id>/books/<book_id>", methods=["POST"])
def add_book_to_author_by_id(author_id):
    author = Author.query.get_or_404(author_id)
    book = Book.query.get_or_404(book_id)
    author.books.append(book)
    db.session.add(author)
    db.session.commit()
    ret = author.to_json(entities=True)
    return jsonify(ret)
