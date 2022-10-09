from flask_app.config.mysqlconnection import connectToMySQL
import re 
from flask import flash, session
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Email: 
    def __init__(self, data):
        self.id = data["id"]
        self.email_address = data["email_address"]
        self.created_at = data["created_at"]

    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM emails;"
        results = connectToMySQL('email_schema').query_db(query)

        if results:
            emails = []

            for email in results:
                emails.append(cls(email))
            return emails
    
    @classmethod
    def insert(cls, data):
        query = "INSERT INTO emails (email_address)"
        query += "VALUES(%(email_address)s);"
        return connectToMySQL('email_schema').query_db(query,data)

    @classmethod
    def getCreatedEmail(cls):
        query = "SELECT * FROM emails ORDER BY ID DESC LIMIT 1;"
        user = connectToMySQL('email_schema').query_db(query)
        if(user):
            return cls(user[0])

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM emails WHERE id=%(id)s;"
        return connectToMySQL('email_schema').query_db(query,data)

    @staticmethod
    def validate_email(email):
        is_valid = True
        if not EMAIL_REGEX.match(email['email_address']):
            flash("Invalid email address")
            is_valid = False
        if 'emails' in session:
            print("IN")
            print(session['emails'])
            for key in session["emails"]:
                print(key)
                if session["emails"][key] == email['email_address']:
                    flash("NOT A UNIQUE EMAIL ADDRESS")
                    is_valid = False
        return is_valid