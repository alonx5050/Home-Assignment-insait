
# Backend Developer Task

Welcome to my repository for the Backend Developer Task! This project demonstrates a simple Flask-based application integrated with OpenAI’s API for answering questions, storing them in a PostgreSQL database. The project is fully containerized using Docker, and pytest has been used for testing.

## Table of Contents
1. [Overview](#overview)
2. [Technologies Used](#technologies-used)
3. [Setup & Installation](#setup--installation)
4. [How to Run the Application](#how-to-run-the-application)
5. [Running Tests](#running-tests)
6. [Database Migrations](#database-migrations)
7. [Best Practices for DAL](#best-practices-for-dal)
8. [Deliverables](#deliverables)

---

## Overview

This Flask application allows users to ask questions via a POST request, and the answers are fetched using OpenAI's GPT-4 model. The questions and answers are then saved in a PostgreSQL database. The whole system is dockerized, making it easy to deploy and scale.

---

## Technologies Used

- **Flask**: Web framework for building the API.
- **PostgreSQL**: For storing the questions and answers.
- **SQLAlchemy**: For ORM and database interactions.
- **Alembic**: For database migrations.
- **Docker**: Containerization of the application and database.
- **Pytest**: For testing the Flask application.

---

## Setup & Installation

### Prerequisites

- Docker
- Python 3.11 or higher
- PostgreSQL 

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/alonx5050/backend-developer-task.git
   cd backend-developer-task
   ```

2. creating the virtual environment:
   ```bash
   python -m venv venv
   ```

3. active the virtual enviroment:
   for windows:
   ```bash
   .\venv\Scripts\activate
   ```   
   for mac:
   ```bash
   source venv/bin/activate
   ``` 


2. Create a `.env` file to store your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ```

3. Build and start the Docker containers:
   ```bash
   docker-compose up --build
   ```

4. The application will now be running on `http://127.0.0.1:5000`.

---

## How to Run the Application

Once you have the Docker containers running, you can interact with the application using Postman or curl.

### Example Request:

- **Endpoint**: `/ask`
- **Method**: POST
- **Headers**: Content-Type - application/json
- **Body** (JSON):
  ```json
  {
    "question": "What is the capital of France?"
  }
  ```

### How to View Questions and Answers in PostgreSQL

To view the questions and answers stored in your PostgreSQL database, you can follow these steps:

#### 1. Connect to Your PostgreSQL Database
First, open a terminal and run the following command inside your Flask app Docker container to connect to the database:

```bash
docker exec -it backend-developer-task-db-1 /bin/sh
```

Once inside the container, connect to the PostgreSQL instance using the `psql` client:

```bash
psql -h localhost -U user -d qna_db
```

You’ll be prompted to enter the password (use `password` as per your `docker-compose.yml` file).

#### 2. View the Table Structure
To check if the `QnA` table was created, you can list all the tables in the database:

```sql
\dt
```

You should see a table named `qn_a` (or whatever table name was defined in your model).

#### 3. Query the Data
To view the questions and answers, you can run the following SQL `SELECT` query:

```sql
SELECT * FROM qn_a;
```

This will return all the rows with the questions and their corresponding answers stored in the database.

#### 4. Exit
Once you're done, you can exit the `psql` terminal by typing:

```sql
\q
```

Then, exit the Docker container by typing:

```bash
exit
```

---

## Running Tests

I’ve implemented one test using pytest to ensure the `/ask` endpoint works as expected.

1. Install the necessary test requirements:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the tests:
   ```bash
   pytest test_app.py
   ```

---

## Database Migrations

The project uses Alembic for database migrations. After making changes to the model, you can generate a new migration and apply it.

### Steps:

1. **Create a migration**:
   ```bash
   docker exec -it <flask-container-name> alembic revision --autogenerate -m "Your migration message"
   ```

2. **Apply the migration**:
   ```bash
   docker exec -it <flask-container-name> alembic upgrade head
   ```

---

## Best Practices for DAL

###  SQLAlchemy as an ORM (Object Relational Mapper)
We have used SQLAlchemy to interact with the PostgreSQL database. This provides a high-level abstraction over raw SQL queries, improving code readability and maintainability. It allows us to easily map Python objects (our `QnA` model) to database tables and perform queries in a more Pythonic way. 

###  Use of Context Management
In the project, we utilize `app.app_context()` to handle operations that require a Flask application context. This ensures that the database session is tied to the application’s lifecycle, allowing for safe and efficient handling of database transactions, as well as the automatic closing of connections after operations are completed.

This is crucial for maintaining the stability of the application and preventing potential issues with dangling database connections.

###  Query Filtering
For querying the database, we use `QnA.query.filter_by()`, which leverages SQLAlchemy’s ORM capabilities to dynamically construct SQL queries based on our model. This approach ensures that queries are efficient, readable, and easy to modify if needed.

###  Transaction Management
Inserting new records into the database follows proper transaction management using `db.session.add()` and `db.session.commit()`. These ensure that each operation is handled as a transaction. If something fails during the process, SQLAlchemy will automatically handle rollback operations, keeping the database in a consistent state.

This ensures data integrity and prevents partial updates that could corrupt the database.

###  Using Migrations with Alembic
The project is configured with Alembic for database migrations. This allows us to track and apply database schema changes consistently across different environments, ensuring the same schema structure exists in development, staging, and production.
We have also implemented **automatic migrations** using Alembic, which helps ensure database schema consistency across environments. This allows us to apply database schema changes safely and automatically.

Alembic helps prevent potential conflicts in schema versions and ensures smooth database upgrades.
---

