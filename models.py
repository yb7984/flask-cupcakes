"""Models for Cupcake app."""

from flask_sqlalchemy import SQLAlchemy,sqlalchemy
import os

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class Cupcake(db.Model):
    """Cupcake."""

    __tablename__ = "cupcakes"


    id = db.Column(db.Integer , primary_key=True , autoincrement=True)
    flavor = db.Column(db.Text , nullable=False)
    size = db.Column(db.Text , nullable=False)
    rating = db.Column(db.Float , nullable=False)
    image = db.Column(db.Text , nullable=False , server_default='https://tinyurl.com/demo-cupcake')

    def __repr__(self):
        """Return better representation for Cupcake"""
        return f'<Cupcake id={self.id} flavor={self.flavor} size={self.size}>'

    def serialize(self):
        """Serialize a dessert SQLAlchemy obj to dictionary."""

        return {
            "id" : self.id ,
            "flavor" : self.flavor ,
            "size" : self.size ,
            "rating" : self.rating ,
            "image" : self.image
        }
