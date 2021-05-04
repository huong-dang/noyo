import uuid
import json

from flask import request, abort, jsonify
from flask_restplus import Resource, Namespace
from models.person import PersonModel, OUTPUT_FIELDS, USER_INPUT_FIELDS
from schemas.person import PersonSchema
from request.person import PersonRequestSchema
from marshmallow import ValidationError
from util.helper import is_uuid, is_different

person_ns = Namespace('person', description='Person related operations')

class Person(Resource):
    def get(self, id):
        """Fetch the latest version of a single person using their id; if version is provided, fetch a single person using their id and the specified version"""
        try:
            valid_id = is_uuid(id)
            version = request.args.get('version', '')
            person_schema = PersonSchema(only=OUTPUT_FIELDS)
            if valid_id and version:
                person_data = PersonModel.find_by_id_and_version(id, version)
                if person_data:
                    return person_schema.dump(person_data)
                else:
                    return {'message': f"Resource not found"}, 404
            elif valid_id:
                person_data = PersonModel.find_by_id(id)
                if person_data:
                    return person_schema.dump(person_data)
                else:
                    return {'message': f"Resource not found"}, 404
            else:
                return {'message': f"Resource not found"}, 404  
        except Exception as error:
            print(error)
            return "Internal Server Error", 500
    
    def patch(self, id):
        """Update a single person using their id"""
        try:
            valid_id = is_uuid(id)
            if valid_id:
                person_data = PersonModel.find_by_id(id)
                if person_data:
                    original_data = person_data.json()
                    request_data = request.get_json()       
                    schema = PersonRequestSchema()       
                    proposed_modification = schema.load(request_data, partial=True)
                    
                    if proposed_modification and is_different(proposed_modification, original_data, USER_INPUT_FIELDS):
                        updated_person = PersonModel(
                            id=person_data.id,
                            first_name=proposed_modification.get('first_name') or original_data.get('first_name'),
                            middle_name=proposed_modification.get('middle_name') or original_data.get('middle_name'),
                            last_name=proposed_modification.get('last_name') or original_data.get('last_name'),
                            age=proposed_modification.get('age') or original_data.get('age'),
                            email=proposed_modification.get('email') or original_data.get('email'),
                            version=original_data.get('version') + 1, 
                            latest=True
                        )
                        updated_person.save_to_db()
                        # The original person object is no longer the latest
                        person_data.latest = False
                        person_data.save_to_db()
                        return {'message': f"Successfully updated person with id: {id}"}
                    else:
                        return {'message': f"No changes detected from user input versus database record"}
                else:
                    return {'message': f"Resource not found"}, 404
            else:
                return {'message': f"Resource not found"}, 404
        except ValidationError as error:
            return error.messages, 400
        except Exception as error:
            print(error)
            return "Internal Server Error", 500
    
    def delete(self, id):
        """Delete a single person using their id"""
        try:
            valid_id = is_uuid(id)
            if valid_id:
                person = PersonModel.find_by_id(id)
                if person:
                    person.delete_from_db()
                    return {'message': f"Successfully deleted person with id: {person.id} and version: {person.version}"}
                else:
                    return {'message': f"Resource not found"}, 404  
            else:
                return {'message': f"Resource not found"}, 404  
        except Exception as error:
            print(error)
            return "Internal Server Error", 500

class PersonsList(Resource):
    def get(self):
        """Fetch a list of all persons (latest version)"""
        persons_list_schema = PersonSchema(many=True, only=OUTPUT_FIELDS)
        return persons_list_schema.dump(PersonModel.find_all())

    def post(self):
        """Create a new person"""
        try:
            request_data = request.get_json()
            schema = PersonRequestSchema()
            new_person_request = schema.load(request_data)        
            unique_id = uuid.uuid4()
            first_name = new_person_request.get('first_name')
            middle_name = new_person_request.get('middle_name')
            last_name = new_person_request.get('last_name')
            print(new_person_request)
            is_unique_name = PersonModel.is_unique(first_name, middle_name, last_name)
            if is_unique_name:
                person = PersonModel(
                            id=unique_id, 
                            first_name=new_person_request.get('first_name'),
                            middle_name=new_person_request.get('middle_name'),
                            last_name=new_person_request.get('last_name'),
                            age=new_person_request.get('age'),
                            email=new_person_request.get('email'),
                            version=1,
                            latest=True
                        )
                person.save_to_db()
                return {
                            "message": f"Person successfully created!", 
                            "id": str(person.id)
                }, 201
            else:
                return {
                    "message": "Resource with the specified name identifier already exists"
                }, 409
        except ValidationError as error:
            return error.messages, 400
        except Exception as error:
            print(error)
            return "Internal Server Error", 500