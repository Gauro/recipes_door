from app.models import Recipe

username = 'gaurav'
password = 'gaurav'


created_recipe = Recipe()


def test_create_recipe(client):
    # Assuming you have a function to log in the user and you have a user logged in
    # For example, you can use Flask-Login to manage user authentication
    client.post('/login', data={'username': username, 'password': password})
    # Create a new recipe
    recipe_data = {
        'title': 'Test Recipe',
        'description': 'This is a test recipe',
        'ingredients': 'Ingredient 1, Ingredient 2',
        'instructions': 'Step 1, Step 2'
    }

    # Make a POST request to the endpoint that adds a new recipe
    response = client.post('/recipe/add', data=recipe_data)

    # Check if the recipe was created successfully (status code 200 or 201 depending on your implementation)
    assert response.status_code == 200  # Update as needed

    # Optionally, you can check if the recipe exists in the database
    global created_recipe
    created_recipe = Recipe.query.filter_by(title='Test Recipe').first()
    assert created_recipe is not None


def test_delete_recipe(client):
    # Make a POST request to the endpoint that deletes the recipe
    client.post('/login', data={'username': username, 'password': password})
    response = client.post(f'/recipe/delete/{created_recipe.id}')

    # Check if the recipe was deleted successfully (status code 200 or 204 depending on your implementation)
    assert response.status_code == 200  # Update as needed

    # Optionally, you can check if the recipe no longer exists in the database
    deleted_recipe = Recipe.query.filter_by(title='Test Recipe test').first()
    assert deleted_recipe is None
