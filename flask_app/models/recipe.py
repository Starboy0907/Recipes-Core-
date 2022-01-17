from ..config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class Recipe:
    db_name = 'recipe_schema'
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.under_30_min = data['under_30_min']
        self.description = data['description']
        self.instructions = data['instructions']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']
        

    @staticmethod
    def validate(recipe):
        isValid = True
        query = "SELECT * FROM recipes WHERE id  = %(id)s;"
        results = connectToMySQL(Recipe.db_name).query_db(query,recipe)
        if len(recipe['name']) < 6:
            isValid = False
            flash("Name must be at least 3 characters long")
        if len(recipe['description']) < 3:
            isValid = False 
            flash("Description must be at least 3 characters long")
        if len(recipe['instructions']) < 3:
            isValid = False 
            flash("Instructions name must be at least 3 characters long")
        return isValid

    @classmethod
    def save(cls, data):
        query = "INSERT INTO recipes (name, description, under_30_min, instructions, date_made, created_at, updated_at, users_id) VALUES (%(name)s, %(description)s, %(under_30_min)s, %(instructions)s, %(date_made)s, NOW(), NOW(), %(users_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL(cls.db_name).query_db(query)
        recipes = []
        for recipe in results:
            recipes.append(cls(recipe))
        return recipes

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def email(cls, data):
        query = "SELECT * FROM recipes WHERE email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def update(cls,data):
        query = "UPDATE recipes SET name = %(name)s, under_30_min = %(under_30_min)s, description = %(description)s, instructions = %(instructions)s, created_at = NOW(), updated_at = NOW(), users_id = %(users_id)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)


