# 📝 Todo List API

This project is a backend API built with **Django**, **Django REST Framework**, and **Strawberry GraphQL**, for managing a task list. It provides both RESTful and GraphQL interfaces, as well as interactive documentation via **Swagger** and **GraphiQL**.

---

## 🚀 Tech Stack

- Python 3.10+
- Django 5.x
- Django REST Framework
- Strawberry GraphQL
- SQLite (for testing)
- PostgresSQL (Image)
- Docker + Docker Compose
- Pytest (for testing)
- drf-spectacular (for Swagger docs)

---

## ⚙️ Requirements

- Python 3.10+
- Docker + Docker Compose
- Poetry

---

## 🔧 Installation (Local)

Clone the repository and install dependencies:

```bash
git clone https://github.com/your-username/todo-list-app.git
cd todo-list-app
poetry install
```

---

## 🧪 Running Tests

To run the full test suite:

```bash
pytest
```

With test coverage:

```bash
pytest --cov=core
```

## 🧼 Flake8 and Black

To run flake8 and black formatter:

```bash
flake8 .
```

```bash
black .
```

---

## 🐳 Running

Replace `.env_example` with your own `.env` or use the same variables.

Build and start the containers:

```bash
docker build .
docker-compose build
docker-compose up
```

The app will be available at:  
📍 [`http://localhost:8000`](http://localhost:8000)

---

## 🔐 Django Admin & Superuser

To create a Django superuser inside the Docker container, run:

```bash
docker-compose run --rm app sh -c "python3 manage.py createsuperuser"
```

Then follow the prompts to enter username, email, and password.

Once created, you can access the Django admin interface at:  
🔑 [`http://localhost:8000/admin/`](http://localhost:8000/admin/)

---

## 📬 Available Endpoints

### 🔹 REST API (DRF)

- `GET     /api/tasks/`
- `POST    /api/tasks/`
- `GET     /api/tasks/<id>/`
- `PUT     /api/tasks/<id>/`
- `DELETE  /api/tasks/<id>/`

### 🔹 GraphQL API

- `POST /graphql/`  
  → Access the GraphiQL UI in your browser for queries and mutations.

---

## 📚 API Documentation

- 📘 Swagger UI: [`/api/docs/`](http://localhost:8000/api/docs/)
- 🧾 OpenAPI schema (JSON): [`/api/schema/`](http://localhost:8000/api/schema/)
- 🧠 GraphiQL: [`/graphql/`](http://localhost:8000/graphql/)

---

## 📁 Project Structure

```
todo_list_app/
├── app/                      # Main Django settings and URLs
├── core/                     # Models and business logic
├── todolist/                 # REST API views and serializers - Graphql logic
├── tests/                    # Unit and integration tests
├── docker-compose.yml
├── requirements.txt / pyproject.toml
├── manage.py
└── README.md
```

---

## ✨ Author

Built with ❤️ by **Ana**
