"""ORM for the Postgresql Persons table"""
import uuid
from db import db 
from typing import List
from sqlalchemy.dialects.postgresql import UUID

# Define the fields that can be modified via user input
USER_INPUT_FIELDS = ['email', 'age', 'first_name', 'last_name', 'middle_name']
# Define the fields shown to the client about a Person entity
OUTPUT_FIELDS = ['first_name', 'middle_name', 'last_name', 'email', 'age', 'latest', 'version', 'id']

class PersonModel(db.Model):
    __tablename__ = 'Persons'
    
    person_id = db.Column(db.Integer, primary_key=True)
    id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(1000), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    version = db.Column(db.Integer, nullable=False)
    latest = db.Column(db.Boolean, nullable=False)

    def __init__(self, id, first_name, middle_name, last_name, email, age, version, latest):
        self.id = id
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.email = email
        self.age = age
        self.version = version
        self.latest = latest
    
    def __repr__(self):
        return "PersonModel(person_id=%s, id=%s, first_name=%s, middle_name=%s, last_name=%s, email=%s, age=%s, version=%s, latest=%s)" \
            % (self.person_id, self.id, self.first_name, self.middle_name, self.last_name, self.email, self.age, self.version, self.latest)

    def json(self):
        return {
            "first_name": self.first_name, 
            "last_name": self.last_name,
            "middle_name": self.middle_name,
            "age": self.age,
            "email": self.email,
            "id": self.id,
            "version": self.version
        }    

    @classmethod
    def find_by_id(cls, id) -> "PersonModel":
        return cls.query.filter_by(id=id, latest=True).first()
    
    @classmethod
    def find_by_id_and_version(cls, id, version) -> "PersonModel":
        return cls.query.filter_by(id=id, version=version).first()

    @classmethod
    def is_unique(cls, first_name, middle_name, last_name) -> "PersonModel":
        result = cls.query.filter_by(first_name=first_name, middle_name=middle_name, last_name=last_name).first()
        return not result


    @classmethod
    def find_all(cls) -> List["PersonModel"]:
        return cls.query.filter_by(latest=True).all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()