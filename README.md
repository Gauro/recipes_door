# Recipes Door

Recipes Door is a web application for managing and sharing recipes. It allows users to register, login, create, view, edit, and delete recipes.

## Overview

The project structure includes the following components:

- `app`: Contains the Flask application code.
  - `__init__.py`: Initializes the Flask app and sets up database configurations.
  - `models.py`: Defines database models using SQLAlchemy for users and recipes.
  - `routes.py`: Defines routes for handling user authentication, recipe CRUD operations, and other functionalities.
  - `templates`: Contains HTML templates for rendering web pages.
- `test`: Contains test files for unit testing the application.
  - `conftest.py`: Sets up testing configurations and fixtures.
  - `test_authentication.py`: Contains tests related to user authentication.
  - `test_recipe.py`: Contains tests related to recipe functionalities.
- `config.py`: Configuration file for the application.
- `requirements.txt`: Lists all required Python packages and their versions.
- `db_script.sql`: SQL script to create the database schema.
- `run.py`: Entry point for running the Flask application.

## Setup Instructions

To set up and run the Recipes Door application, follow these steps:

1. Clone the repository:
  git clone https://github.com/Gauro/recipes_door.git

2. Navigate to the project directory:
  cd recipes_door

3. Create the database schema using the provided SQL script:
  mysql -u <username> -p < db_script.sql

4. Run the application
  python run.py

5. Access the application in your web browser at http://localhost:5000

## Endpoints
### Authentication
- /register: Register a new user.
- /login: Log in with username and password.
- /logout: Log out the current user.

### Recipes
- /: Homepage.
- /user_recipe: View recipes created by the logged-in user.
- /recipe_all: View all recipes.
- /recipe/add: Add a new recipe.
- /recipe/<int:id>: View details of a specific recipe.
- /recipe/<int:id>/edit: Edit a recipe.
- /recipe/delete/<int:id>: Delete a recipe.

## Additional Notes
- Flask-Login is used for user authentication and session management.
- SQLAlchemy is used as the ORM for interacting with the database.
- The application is tested using pytest for unit testing.