# Task Manager API

A simple Task Manager REST API built using **Python and FastAPI**.

I built this project to learn how a backend API works with a real database, user authentication, and CRUD operations.

## Tech Used

* Python
* FastAPI
* MySQL
* SQLAlchemy
* PyMySQL
* JWT Authentication
* Python-Jose
* Passlib + Bcrypt
* Python-Dotenv
* Swagger UI

## What this project can do

* Create a user account
* Hash user passwords before storing them
* Login and get a JWT access token
* Create tasks
* View tasks
* View a single task
* Update tasks
* Delete tasks
* Filter tasks by completed status
* Allow users to access only their own tasks
* Store data in MySQL
* Test all APIs using Swagger UI


## Project Structure

```text
task-manager/
│
├── main.py
├── database.py
├── models.py
├── schemas.py
├── oauth2.py
├── utils.py
│
├── routers/
│   ├── auth.py
│   ├── user.py
│   └── task.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## What each file does

* `main.py` - Starts the FastAPI application and connects the routers.
* `database.py` - Creates the MySQL database connection and database sessions.
* `models.py` - Contains the SQLAlchemy database models for users and tasks.
* `schemas.py` - Validates request data and defines response formats.
* `oauth2.py` - Handles JWT tokens and gets the current logged-in user.
* `utils.py` - Handles password hashing and password verification.
* `routers/auth.py` - Handles user login and JWT token creation.
* `routers/user.py` - Handles user registration and getting users.
* `routers/task.py` - Handles task CRUD operations.
* `.env` - Stores database and JWT configuration.
* `.gitignore` - Prevents files such as `.env` and `venv` from being pushed to GitHub.
* `requirements.txt` - Contains the Python packages required for the project.


## Database

The project uses two tables:

### Users

```text
users
-------------------------
id
email
password
created_at
```

### Tasks

```text
tasks
-------------------------
id
title
description
completed
created_at
owner_id
```

`owner_id` is a foreign key connected to the `users` table.

```text
users
  │
  │ 1
  │
  └────────── * tasks
```

This allows each task to belong to a particular user.

## Authentication

The API uses JWT authentication.

The basic flow is:

```text
Register
   ↓
Password is hashed
   ↓
User saved in MySQL
   ↓
Login
   ↓
Password is verified
   ↓
JWT token is created
   ↓
Token is used for protected routes
```

The JWT token is also configured with an expiration time.



## API Endpoints

### Users

| Method | URL           | Purpose           |
| ------ | ------------- | ----------------- |
| POST   | `/users/`     | Create a new user |
| GET    | `/users/{id}` | Get a user        |

### Authentication

| Method | URL      | Purpose                 |
| ------ | -------- | ----------------------- |
| POST   | `/login` | Login and get JWT token |

### Tasks

| Method | URL           | Purpose          |
| ------ | ------------- | ---------------- |
| POST   | `/tasks/`     | Create a task    |
| GET    | `/tasks/`     | Get user's tasks |
| GET    | `/tasks/{id}` | Get one task     |
| PUT    | `/tasks/{id}` | Update a task    |
| DELETE | `/tasks/{id}` | Delete a task    |

Tasks endpoints require authentication.

## Example

### Create Task

After logging in and authorizing with the JWT token in Swagger:

```json
{
  "title": "Learn FastAPI",
  "description": "Complete Task Manager project",
  "completed": false
}
```

The task is automatically connected to the logged-in user using their `owner_id`.

## Update a Task

The update endpoint supports updating only the fields that are sent.

For example:

```json
{
  "completed": true
}
```

This changes the completion status without changing the other task information.

## Install & Running the Project

### 1. Clone the repository

```bash
git clone <your-repository-url>
```

### 2. Go to the project folder

```bash
cd task-manager
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

Windows:

```powershell
venv\Scripts\Activate.ps1
```

### 5. Install the required packages

```bash
pip install -r requirements.txt
```

### 6. Create the MySQL database

```sql
CREATE DATABASE task_manager;
```

### 7. Create a `.env` file

Add your database and JWT settings:

```env
SQLALCHEMY_DATABASE_URL=mysql+pymysql://USERNAME:PASSWORD@localhost/task_manager

SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 8. Start the FastAPI server

```bash
uvicorn main:app --reload
```

The API will run at:

```text
http://127.0.0.1:8000
```


## Swagger API Documentation

FastAPI provides Swagger UI automatically.

Open:

```text
http://127.0.0.1:8000/docs
```

I used Swagger UI to test the API instead of building a separate frontend.

From Swagger, you can:

1. Register a user
2. Login
3. Get the JWT token
4. Authorize the API
5. Create tasks
6. View tasks
7. Update tasks
8. Delete tasks


## What I Learned

While building this project, I learned how to:

* Build REST APIs using FastAPI
* Use path and query parameters
* Validate data using Pydantic
* Use response models
* Connect FastAPI with MySQL
* Use SQLAlchemy ORM
* Create database relationships
* Perform CRUD operations
* Use FastAPI dependencies
* Hash passwords using bcrypt
* Implement JWT authentication
* Protect API routes
* Check task ownership
* Use environment variables
* Test APIs using Swagger UI
* Manage a project using Git and GitHub

## Project Goal

I built this project as a learning and portfolio project to get practical experience in **Python backend development and FastAPI**.
