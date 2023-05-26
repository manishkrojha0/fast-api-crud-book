# Book Management API

# BOOK CRUD USING FASTAPI FRAMEWORK
This is a RESTful API for managing books. It provides endpoints to perform CRUD operations on books and user authentication.

## Endpoints

The following endpoints are available:

- `POST /register`: Register a new user.
- `POST /login`: Log in with a username and password to obtain an access token.
- `GET /books`: Retrieve a paginated list of all books.
- `GET /books/{book_id}`: Retrieve details of a specific book by its ID.
- `POST /books`: Create a new book.
- `PUT /books/{book_id}`: Update the details of a specific book by its ID.
- `DELETE /books/{book_id}`: Delete a book by its ID.

## Setup

To set up the project, follow these steps:

1. Clone the repository: `git clone <repository-url>`
2. Create and activate a virtual environment: `python -m venv env` and `source env/bin/activate`
3. Install the dependencies: `pip install -r requirements.txt`
4. Set up the database: `alembic upgrade head`
5. Start the development server: `uvicorn main:app --reload`

Note: Make sure to configure the database connection in the `.env` file.

## Testing

To run the tests, use the following command:

