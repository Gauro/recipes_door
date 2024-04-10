username = 'gaurav'
password = 'gaurav'


def test_user_registration(client):
    response = client.post('/register', data={'username': username, 'password': password})
    assert response.status_code == 302
    assert b'User successfully registered'


def test_user_login_positive(client):
    response = client.post('/login', data={'username': username, 'password': password})
    assert response.status_code == 200
    assert b'Login successful'


def test_user_login_wrong_password(client):
    response = client.post('/login', data={'username': username, 'password': 'incorrect_password'})
    assert response.status_code == 401  # Assuming 401 Unauthorized status code for wrong password
    assert b'Incorrect username or password' in response.data


def test_user_login_wrong_username(client):
    response = client.post('/login', data={'username': "wrong_username", 'password': password})
    assert response.status_code == 401  # Assuming 401 Unauthorized status code for wrong password
    assert b'Incorrect username or password' in response.data


def test_user_login_wrong_negative(client):
    response = client.post('/login', data={'username': "wrong_username", 'password': 'incorrect_password'})
    assert response.status_code == 401  # Assuming 401 Unauthorized status code for wrong password
    assert b'Incorrect username or password' in response.data


def test_user_login_missing_username(client):
    response = client.post('/login', data={'password': 'password123'})
    assert response.status_code == 400  # Assuming 400 Bad Request status code for missing username
    assert b'Missing username' in response.data  # Assuming the response contains a message indicating missing username


def test_user_logout(client):
    # Now, make the request to the logout route
    client.post('/login', data={'username': username, 'password': password})
    response = client.get('/logout')

    # Check if the response status code is 302 (redirect)
    assert response.status_code == 302
