from library import db
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


books_authors = db.Table(
    "books_authors",
    db.Column("book_id", db.Integer, db.ForeignKey("book.id"), primary_key=True),
    db.Column("author_id", db.Integer, db.ForeignKey("author.id"), primary_key=True),
)


class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    due_date = db.Column("due_date", db.DateTime())
    book = db.Column("book_id", db.Integer, db.ForeignKey("book.id"))
    user = db.Column("user_id", db.Integer, db.ForeignKey("user.id"))


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    books = db.relationship(
        "Book",
        secondary=books_authors,
        lazy="subquery",
        backref=db.backref("authors", lazy=True),
    )

    def to_json(self, entities=False):
        if not entities:
            return {"name": self.name, "id": self.id}
        else:
            return {
                "name": self.name,
                "id": self.id,
                "books": [book.title for book in self.books],
            }


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    isbn = db.Column(db.String())


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    barcode = db.Column(db.String())
    membertype = db.Column(db.String())
    # loans = db.relationship(
    #     "Book",
    #     secondary="loan",
    #     lazy="subquery",
    #     backref=db.backref("user", uselist=False, lazy=True),
    # )


if __name__ == "__main__":
    db.create_all()
    book1 = Book(title="How to Draw Good", isbn="3289589036")
    book2 = Book(title="Making the Cake", isbn="23567035")
    book3 = Book(title="Laughing for No Reason", isbn="3297806")
    author1 = Author(name="Arthur James")
    author2 = Author(name="Evelyn Dorothy")
    author3 = Author(name="Lisa Jones")
    book1.authors.append(author1)
    book2.authors.append(author3)
    book3.authors.append(author2)
    book3.authors.append(author1)
    user1 = User(name="Martin Chorley", barcode="123456", membertype="Staff")
    db.session.add(book1)
    db.session.add(book2)
    db.session.add(book3)
    db.session.add(author1)
    db.session.add(author2)
    db.session.add(author3)
    db.session.add(user1)
    db.session.commit()
    loan = Loan(
        due_date=datetime.fromisoformat("2020-05-06"), book=book1.id, user=user1.id
    )
    db.session.add(loan)
    db.session.commit()
