from flask_app import app
from flask import Flask, render_template, redirect, session, request
from flask_app.models.user import User
from flask_app.models.recipe import Recipe 

from flask import flash

@app.route('/dashboard')
def dash():
    # call the get all classmethod to get all recipes
    recipes = Recipe.get_all()
    print(recipes)
    return render_template('dashboard.html',all_users=User.getAll(),user=User.getOne({'id': session['user_id']}), all_recipes = recipes )



@app.route('/recipes/<int:id>')
def show(id):
    data = {
        "id" : id
    }
    recipes = Recipe.get_one(data)
    print(recipes)
    return render_template('recipes.html', one_recipe = recipes)

@app.route('/add_recipe', methods=['POST'])
def add_recipe():
    print(request.form)
    if not Recipe.validate(request.form):
        # redirect to the route where the burger form is rendered.
        return redirect('/recipe/new')
    # else no errors:
    Recipe.save(request.form)
    return redirect('/dashboard')

@app.route('/recipe/new')
def new():
    recipes = Recipe.save
    return render_template('new_recipe.html', recipes = recipes)

@app.route('/edit_recipe', methods=['POST'])
def edit():
    print(request.form)
    if not Recipe.validate(request.form):
        # redirect to the route where the burger form is rendered.
        return redirect('/recipe/edit/<int:id>')
    Recipe.update(request.form)
    return redirect('/recipe/<int:id>')

@app.route('/recipes/edit/<int:id>')
def update(id):
    data = {
        "id" : id
    }
    recipe = Recipe.get_one(data)
    recipes = Recipe.update
    return render_template('edit_recipe.html', one_recipe = recipe, recipes=recipes,  id=id)

@app.route('/delete/<int:id>')
def delete(id):
    recipes = Recipe.delete()
    return redirect('/dashboard')



