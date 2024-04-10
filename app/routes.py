import secrets

from flask import Flask, jsonify
from flask import render_template, redirect, url_for, request, flash
from flask_login import LoginManager
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import or_
from werkzeug.security import check_password_hash, generate_password_hash

from app.models import User, Recipe
from app.models import db

recipes_per_page = 5

app = Flask(__name__)

# Configure SQLAlchemy to use MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root123@localhost:3306/Recipe'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Generate a random secret key
secret_key = secrets.token_hex(16)

# Set the secret key for the application
app.secret_key = secret_key


# Homepage route
@app.route('/')
def index():
    return render_template('base.html')


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


# Authentication routes
# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username:
            # Return 400 status code for missing username
            return jsonify({'message': 'Missing username'}), 400
        if not password:
            # Return 400 status code for missing password
            return jsonify({'message': 'Missing password'}), 400

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)

            # Fetch recipes for the logged-in user
            user_recipes = Recipe.query.filter_by(created_by=current_user.id).paginate(page=1,
                                                                                       per_page=recipes_per_page)

            # Calculate total pages for user's recipes
            total_pages = user_recipes.pages

            # Get the current page number for user's recipes
            current_page = user_recipes.page

            # Pass the recipes to the template
            return render_template('recipe_list.html', recipes=user_recipes, total_pages=total_pages,
                                   current_page=current_page, user_id=current_user.id)
        else:
            # flash('Invalid username or password', 'error')
            # Return 401 status code for failed login attempts
            return jsonify({'message': 'Incorrect username or password'}), 401
    return render_template('login.html')


@app.route('/user_recipe', methods=['GET', 'POST'])
@login_required
def user_recipe():
    # Fetch recipes for the logged-in user

    user_recipes = Recipe.query.filter_by(created_by=current_user.id).paginate(page=1,
                                                                               per_page=recipes_per_page)

    # Calculate total pages for user's recipes
    total_pages = user_recipes.pages

    # Get the current page number for user's recipes
    current_page = user_recipes.page

    # Pass the recipes to the template
    # return render_template('recipe_list.html', recipes=user_recipes)
    return render_template('recipe_list.html', recipes=user_recipes, total_pages=total_pages,
                           current_page=current_page, user_id=current_user.id)


@app.route('/recipe_all', methods=['GET', 'POST'])
@login_required
def recipe_all():
    user_recipes = Recipe.query.paginate(page=1, per_page=recipes_per_page)

    # Calculate total pages for user's recipes
    total_pages = user_recipes.pages

    # Get the current page number for user's recipes
    current_page = user_recipes.page

    # Pass the recipes to the template
    # return render_template('recipe_list.html', recipes=user_recipes)
    return render_template('recipe_all.html', recipes=user_recipes, total_pages=total_pages,
                           current_page=current_page, user_id=-1)


# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'error')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))


# CRUD routes for recipes
@app.route('/recipe/add', methods=['GET', 'POST'])
@login_required
def add_recipe():
    # users_ = User.query.all()
    # return render_template('recipe_form.html', current_user=users_)
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        ingredients = request.form.get('ingredients')
        instructions = request.form.get('instructions')

        new_recipe = Recipe(title=title, description=description, ingredients=ingredients, instructions=instructions,
                            created_by=current_user.id)
        db.session.add(new_recipe)
        db.session.commit()
        flash('Recipe added successfully', 'success')

        # Fetch recipes for the logged-in user
        user_recipes = Recipe.query.filter_by(created_by=current_user.id).paginate(page=1,
                                                                                   per_page=recipes_per_page)

        # Calculate total pages for user's recipes
        total_pages = user_recipes.pages
        return render_template('recipe_list.html', recipes=user_recipes, total_pages=total_pages, current_page=1,
                               user_id=current_user.id)

    # return render_template('add_recipe.html')


@app.route('/recipe_form', methods=['GET', 'POST'])
@login_required
def recipe_form():
    users_ = User.query.all()
    return render_template('recipe_form.html', current_user=users_)


# View recipe route
@app.route('/recipe/<int:id>')
def view_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    return render_template('view_recipe.html', recipe=recipe)


# Edit recipe route
@app.route('/recipe/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_recipe(id):
    recipe = Recipe.query.get_or_404(id)

    if request.method == 'POST':
        # recipe.title = request.form.get('title')
        # recipe.description = request.form.get('description')
        # recipe.ingredients = request.form.get('ingredients')
        # recipe.instructions = request.form.get('instructions')
        #
        # db.session.commit()
        # flash('Recipe updated successfully', 'success')
        # return redirect(url_for('view_recipe', id=recipe.id))
        pass

    return render_template('edit_recipe.html', recipe=recipe)
    # # Fetch recipes for the logged-in user
    # user_recipes = Recipe.query.filter_by(created_by=current_user.id).paginate(page=1,
    #                                                                            per_page=recipes_per_page)
    #
    # # Calculate total pages for user's recipes
    # total_pages = user_recipes.pages
    #
    #
    # return render_template('recipe_list.html', recipes=user_recipes, total_pages=total_pages, current_page=1,
    #                    user_id=recipe.created_by)


# Update recipe route
@app.route('/recipe/update/<int:id>/<int:created_by>', methods=['GET', 'POST'])
@login_required
def update_recipe(id, created_by):
    recipe = Recipe.query.get_or_404(id)

    if request.method == 'POST':
        recipe.title = request.form.get('title')
        recipe.description = request.form.get('description')
        recipe.ingredients = request.form.get('ingredients')
        recipe.instructions = request.form.get('instructions')

        db.session.commit()
        flash('Recipe updated successfully', 'success')

        # Fetch recipes for the logged-in user
        user_recipes = Recipe.query.filter_by(created_by=current_user.id).paginate(page=1,
                                                                                   per_page=recipes_per_page)

        # Calculate total pages for user's recipes
        total_pages = user_recipes.pages

        return render_template('recipe_list.html', recipes=user_recipes, total_pages=total_pages, current_page=1,
                               user_id=created_by)

    # return render_template('edit_recipe.html', recipe=recipe)


# Delete recipe route
@app.route('/recipe/delete/<int:id>', methods=['POST'])
@login_required
def delete_recipe(id):
    if request.method == 'POST':
        recipe = Recipe.query.get_or_404(id)
        db.session.delete(recipe)
        db.session.commit()
        flash('Recipe deleted successfully', 'success')

        # Fetch recipes for the logged-in user
        user_recipes = Recipe.query.filter_by(created_by=current_user.id).paginate(page=1,
                                                                                   per_page=recipes_per_page)

        # Calculate total pages for user's recipes
        total_pages = user_recipes.pages

        return render_template('recipe_list.html', recipes=user_recipes, total_pages=total_pages, current_page=1,
                               user_id=recipe.created_by)


@app.route('/recipe/<int:id>')
def recipe_detail(id):
    recipe = get_recipe_by_id(id)  # Replace with your function to retrieve recipe details from the database
    return render_template('recipe_detail.html', recipe=recipe)


def get_recipe_by_id(recipe_id):
    """
    Retrieves recipe details by ID from the database.
    """
    return Recipe.query.get(recipe_id)


@app.route('/search_recipe')
def search_recipe():
    query = request.args.get('query')  # Get the value of the 'query' parameter from the request

    # Perform search logic based on the query
    filtered_recipes = []
    if query:
        filtered_recipes = Recipe.query.filter(
            or_(Recipe.title.ilike(f'%{query}%'), Recipe.ingredients.ilike(f'%{query}%'))
        ).paginate(page=1, per_page=recipes_per_page)

    # Render the search results template with the filtered recipes
    return render_template('recipe_all.html', recipes=filtered_recipes)


@app.route('/page/<int:page>/<int:user_id>')
def page(page, user_id):
    # Get the recipes for the current page
    recipes = Recipe.query.filter_by(created_by=user_id).paginate(page=page, per_page=recipes_per_page)

    # Calculate total pages
    total_pages = recipes.pages

    # Get the current page number
    current_page = recipes.page

    return render_template('recipe_list.html', recipes=recipes, total_pages=total_pages, current_page=current_page,
                           user_id=user_id)
