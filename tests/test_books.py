import json
from fastapi.testclient import TestClient
from core.auth.jwt_auth_handler import signJWT
from core.main import app

client = TestClient(app)

def generate_token():

    user_email = "test_user@example.com"   
    token = signJWT(user_email)
    return token

def test_create_book_with_authentication():
    # Generate a valid token for authentication
    
    token = generate_token()

    # Define the book data
    book_data = {
        "title": "string",
        "publication_date": "string",
        "description": "string",
        "price": 0,
        "author_name": "string"
    }

    # Make a request to the /books endpoint with authentication and book data
    response = client.post("/books", headers={"Authorization": f"Bearer {token}"}, json=book_data)

def test_get_books_with_authentication():
    # Generate a valid token for authentication
    user_email = "test_user@example.com"

    token = generate_token()

    # Make a request to the /books endpoint with authentication
    response = client.get("/books", headers={"Authorization": f"Bearer {token}"})

    # Assert the response status code and content
    assert response.status_code == 200
    assert response.json() == [
                                {
                                    "title": "string",
                                    "publication_date": "string",
                                    "description": "string",
                                    "price": 0,
                                    "author_name": "string"
                                }
                        ]



    # Assert the response status code and content
    assert response.status_code == 201
    assert response.json() == {
                                "title": "string",
                                "publication_date": "string",
                                "description": "string",
                                "price": 0,
                                "id": 0,
                                "author_id": 0
                            }

def test_update_book():
    # Assuming book_id 1 exists in the database
    book_data = {
                    "title": "string",
                    "publication_date": "string",
                    "description": "string",
                    "price": 0
                }
    response = client.put("/books/1", json=book_data)
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json()["title"] == book_data["title"]


def test_update_book_not_found():
    # Assuming book_id 999 does not exist in the database
    book_data = {
                    "title": "string",
                    "publication_date": "string",
                    "description": "string",
                    "price": 0
                }
    response = client.put("/books/999", json=book_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"


def test_delete_book():
    # Assuming book_id 1 exists in the database
    response = client.delete("/books/1")
    assert response.status_code == 204


def test_delete_book_not_found():
    # Assuming book_id 999 does not exist in the database
    response = client.delete("/books/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"
