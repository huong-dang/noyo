import unittest
import os
import json
import copy
import json

from app import create_app
from db import db

class PersonTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.new_person = {
            "first_name": "claire",
            "last_name": "zhang",
            "middle_name": "",
            "age": 20,
            "email": "claire@claire.com"
        }
        self.person_endpoint = "/api/person"
        self.person_id = None

        with self.app.app_context():
            db.create_all()
    
    def test_successful_person_creation(self):
        res = self.client().post(self.person_endpoint, json=self.new_person)
        json_data = res.get_json()
        self.assertEqual(res.status_code, 201)
        self.assertIsNotNone(json_data.get("id"))

    def test_validation_error_person_creation(self):
        new_person = copy.deepcopy(self.new_person)
        new_person['email'] = 1234567890
        res = self.client().post(self.person_endpoint, json=new_person)
        self.assertEqual(res.status_code, 400)
        self.assertIn('email', str(res.data))

    def test_successful_get_person_by_id(self):
        id = self.create_new_person()
        get_person_by_id_endpoint = f"{self.person_endpoint}/{id}"
        res = self.client().get(get_person_by_id_endpoint)
        self.assertEqual(res.status_code, 200)
        self.assertIn(id, str(res.data))

    def test_validation_error_get_person_by_id(self):
        id = 1
        get_person_by_id_endpoint = f"{self.person_endpoint}/{id}"
        res = self.client().get(get_person_by_id_endpoint)
        self.assertEqual(res.status_code, 404)

    def test_successful_person_update(self):
        id = self.create_new_person()
        patch_person_by_id_endpoint = f"{self.person_endpoint}/{id}"
        res = self.client().patch(patch_person_by_id_endpoint, json={"email": "another@another.com"})
        self.assertEqual(res.status_code, 200)
        self.assertIn(id, str(res.data))
    
    def test_successful_person_delete(self):
        id = self.create_new_person()
        patch_person_by_id_endpoint = f"{self.person_endpoint}/{id}"
        res = self.client().patch(patch_person_by_id_endpoint, json={"email": "another@another.com"})
        self.assertEqual(res.status_code, 200)
        self.assertIn(id, str(res.data))

    def test_successful_person_get_all(self):
        id1 = self.create_new_person()
        id2 = self.create_new_person()
        res = self.client().get(self.person_endpoint)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(json.loads(res.data)), 2)

    def test_successful_get_person_by_version_and_id(self):
        id = self.create_new_person()
        # Update the person so database will have a version 2
        self.update_person(id, {"age": 2})
        version = 2
        get_person_by_id_and_version_endpoint = f"{self.person_endpoint}/{id}?version={version}"
        res = self.client().get(get_person_by_id_and_version_endpoint)
        res_data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data.get("latest"), True)
        self.assertEqual(res_data.get("age"), 2)
    
    # Helper function
    def update_person(self, id, payload):
        patch_person_by_id_endpoint = f"{self.person_endpoint}/{id}"
        res = self.client().patch(patch_person_by_id_endpoint, json=payload)

    # Helper function
    def create_new_person(self):
        res = self.client().post(self.person_endpoint, json=self.new_person)
        id = res.get_json().get('id')
        return id

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()
