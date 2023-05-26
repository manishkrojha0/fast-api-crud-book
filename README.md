# Book Management API

# BOOK CRUD USING FASTAPI FRAMEWORK
This is a RESTful API for managing books. It provides endpoints to perform CRUD operations on books and user authentication.

## Getting Started

These instructions will guide you on how to get a copy of the project up and running on your local machine.

### Prerequisites
- Python 3.x
- Git
- Docker

## Setup

To set up the project, follow these steps:

1. Clone the repository: `git clone <repository-url>`
2. Create and activate a virtual environment: `python -m venv env` and `source env/bin/activate`
3. Install the dependencies: `pip install -r requirements.txt`
4. Set up the database: `alembic upgrade head`
5. Start the development server: `uvicorn main:app --reload`

Note: Make sure to configure the database connection in the `.env` file.


## Endpoints

The following endpoints are available:

- `POST /register`: Register a new user.
- `POST /login`: Log in with a username and password to obtain an access token.
- `GET /books`: Retrieve a paginated list of all books.
- `GET /books/{book_id}`: Retrieve details of a specific book by its ID.
- `POST /books`: Create a new book.
- `PUT /books/{book_id}`: Update the details of a specific book by its ID.
- `DELETE /books/{book_id}`: Delete a book by its ID.

## Run the project
- `python main.py`
- Access the application in your web browser at `http://localhost:8000`.
- Access the Swagger file which is the beauty of FastAPI at `http://localhost:8000/docs`. Here you can perform CRUD as well Authentication.

## Running with Docker
- Build the Docker image: `docker build -t bookcrud-api .`
- Run the Docker container: `docker run -p 8000:8000 project-name`
- Access the application in your web browser at: `http://localhost:8000`

# Testing
- To run the test cases, execute the following command: `pytest --rootdir=path-to-your-test-directory`

# Contributing
- Contributions are welcome! To contribute to the project, follow these steps:
  - Fork the repository.
  - Create a new branch for your feature or bug fix.
  - Make your changes and commit them.
  - Push your changes to your forked repository.
  - Submit a pull request to the original repository.
  




