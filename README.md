# Fast_API_Training

A small FastAPI application for training and learning purposes.

## Functionality
The project provides functionality for POST request for creating a shortened version of URLs.
User can retrieve the original URL by providing the shortened version. Or access to root endpoint for getting all URLs from database.
The application uses FastAPI for the API framework, SQLModel for database interactions, and Pydantic for data validation. It is designed to be simple and easy to extend for further experimentation with FastAPI features.

## How to Run
Clone the repository:

```bash
git clone https://github.com/Lampa97/Fast_API_Training.git
```

Navigate to the project directory:
```bash
cd Fast_API_Training
```
Install dependencies with:

```bash
pip install -r requirements.txt
```
Start the application:

```bash
uvicorn main:app --reload
```

Access the API:
Open your browser at http://localhost:8000
API docs available at http://localhost:8000/docs

## Features

- RESTful API endpoints using FastAPI
- SQLite database integration via SQLModel
- Pydantic models for data validation
- Simple URL management (example feature)
- Easily extendable for further experimentation

## Project Structure
- `api/` — Contains API working files
  - `models.py` — SQLModel and Pydantic models
  - `db.py` — Database setup and session management
  - `router.py` — API route definitions
- `urls.db` — SQLite database file (auto-created)
- `main.py` — Application entry point
- `tests/` — Unit and integration tests
- `test.db` — Test database file (auto-created)

## Requirements

- Python 3.10+
- FastAPI
- SQLModel
- Uvicorn
- Pydantic



## Endpoints

Here are the API endpoints defined in `main.py` and `router.py`:

**From `main.py`:**
- **POST `/`**  
  Shorten a given URL and store it in the database.  
  **Request body:** JSON with the original URL.  
  **Response:** JSON with the shortened URL and its code.

- **GET `/`**  
  Retrieve all stored URLs.  
  **Response:** JSON array of all URL records.

- **GET `/{shorten_url}`**  
  Redirect to the original URL based on the shortened URL.  
  **Response:** HTTP redirect (307) to the original URL.

- **DELETE `/{shorten_url}`**  
  Delete a URL record based on the shortened URL.  
  **Response:** JSON with a success message.

The `api/router.py` file defines an endpoint under the `/external` prefix:

- **GET `/external/catfact`**  
  Fetches a random cat fact from an external API (`catfact.ninja`).  
  **Response:** JSON with a random cat fact.

## Testing

To run the tests with extended information, use the following command:

```bash
pytest --cov -vv 
```