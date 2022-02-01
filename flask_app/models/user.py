from ..config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
class User:
    db_name = 'private_wall'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate(user):
        isValid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db_name).query_db(query,user)
        if len(results) >= 1:
            isValid = False
            flash("That username is already in the system!")
        if len(user['password']) < 6:
            isValid = False
            flash("Password must be at least 6 characters long")
        if len(user['first_name']) < 2:
            isValid = False 
            flash("First name must be at least 2 characters long")
        if len(user['last_name']) < 2:
            isValid = False 
            flash("Last name must be at least 2 characters long")
        if len(user['email']) < 2:
            isValid = False 
            flash("Username must be at least 2 characters long")
        if len(user['password']) < 6:
            flash("Password must be at least 6 characters long")
            isValid=False 
        if user['password'] != user['confirm_password']:
            isValid = False
            flash("Your Passwords don't match")
        return isValid


    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def getAll(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db_name).query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def getOne(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def getEmail(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_users_with_messages(cls, data):
        query = "SELECT * from users LEFT JOIN messages ON messages.user_id = users.id WHERE users.id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)
        














        