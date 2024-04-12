from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
import re

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 

    @validates('name')
    def unique_name(self, key, value):
        if value in [author.name for author in Author.query.all()]:
            raise ValueError('That name already exists')
        elif not value:
            raise ValueError('Author must have a name')
        return value
    
    @validates('phone_number')
    def phone_number_length(self, key, value):
        pattern = re.compile(r'[0-9]{10}')
        match = pattern.fullmatch(value)
        if not match:
            raise ValueError('Phone number must be exactly 10 digits')
        return value

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  

    @validates('content')
    def content_length(self, key, value):
        if len(value) < 250:
            raise ValueError('Post content must be at least 250 characters long.')
        return value
    
    @validates('summary')
    def summary_length(self, key, value):
        if len(value) > 250:
            raise ValueError('Post summary must be no more than 250 characters.')
        return value
    
    @validates('category')
    def check_category(self, key, value):
        if value != 'Fiction' and value != 'Non-Fiction':
            raise ValueError('Post category must be either Fiction or Non-Fiction.')
        return value

    @validates('title')
    def check_title(self, key, value):
        strings = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(string in value for string in strings):
            raise ValueError('Title must contain one of the following: "Won\'t Believe", "Secret", "Top", "Guess"')
        return value


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
