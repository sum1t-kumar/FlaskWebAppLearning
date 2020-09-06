
import uuid
from itsdangerous import URLSafeTimedSerializer, TimedJSONWebSignatureSerializer
from flask import current_app
from common.database import Database
from common.utils import Utils
import models.admin.admin_error as AdminErrors
import os
import unicodecsv as csv



class Admin(object):
    COLLECTION = "admin"
    
    def __init__(self, email, password, name=None, company=None, email_valid=None, _id=None, role='member'):
        self.email = email
        self.password = password
        self.name = name
        self.company = company
        self.email_valid = email_valid
        self._id = uuid.uuid4().hex if _id is None else _id
        self.role = role

    def json(self):
        return {
            "_id": self._id,
            "email": self.email,
            "password": self.password,
            "name": self.name,
            "email_valid": self.email_valid,
            "company": self.company
        }

    def save_to_db(self):
        Database.insert(self.COLLECTION, self.json())

    def update_user(self):
        Database.update(self.COLLECTION, query={'email': self.email}, data={'$set': self.json()})

    @staticmethod
    def get_users(query):
        if query:
            user_list = Database.find('users', {'$or': [{'email': {'$regex': query + '.|.'+query+'.', '$options': 'i'}},
                                                                     {'name': {'$regex': query + '.|.'+query+'.', '$options': 'i'}},
                                                                     {'role': {'$regex': query + '.|.'+query+'.', '$options': 'i'}},
                                                                     {'_id': query}
                                                                     ]})

            return user_list
        else:
            user_list = Database.find('users', {})
            return user_list

    @staticmethod
    def delete_user(list_of_users):
        if list_of_users:
            Database.remove('users', {'_id': {'$in': list_of_users}})
            return True
        return False

    @staticmethod
    def export_user(query):
        user_data = []
        list_users = Admin.get_users(query=query)
        for user in list_users:
            user_data.append(user)

        all_cols = []
        for keys in user_data[0].keys():
            all_cols.append(keys)
        print(all_cols)
        directory = os.path.join(current_app.config['EXPORT_PATH'], 'some_static_or_dynamic_file_name.csv')
        with open(directory, 'wb') as output_file:
            dict_writer = csv.DictWriter(output_file, encoding='utf8', errors='ignore', fieldnames=all_cols, quoting=csv.QUOTE_ALL)
            # dict_writer = csv.DictWriter(output_file, fieldnames=fieldnames, encoding='latin1', errors='ignore',
            # quoting=csv.QUOTE_ALL)
            # for non-english data double check once
            dict_writer.writeheader()
            dict_writer.writerows(user_data)

        return 'some_static_or_dynamic_file_name.csv'
