# 📚 Bookly API (FastAPI Backend)

A backend project built using **FastAPI**, **PostgreSQL**, and **SQLAlchemy/SQLModel**.
This project demonstrates building a production-style backend with clean architecture, authentication, and database migrations.

---

## 🚀 Features (Completed So Far)

### 🔹 Core Backend

* FastAPI project setup
* Clean folder structure
* Dependency Injection
* Async database handling

### 🔹 Database

* PostgreSQL integration
* SQLAlchemy / SQLModel ORM usage
* Database session management

### 🔹 CRUD Operations

* Create, Read, Update, Delete APIs for Books
* Service layer separation (business logic)
* Schema validation using Pydantic

### 🔹 Advanced CRUD

* Dynamic update using `setattr`
* Partial updates (`exclude_unset=True`)
* Proper error handling (404, etc.)

### 🔹 Alembic (Database Migrations)

* Migration environment setup
* Auto-generate migrations
* Apply schema changes to database

### 🔹 Authentication (In Progress 🚧)

* User model created
* Signup API
* Login API
* Password hashing using Passlib
* JWT token generation

---

## 🧠 Concepts Learned

* FastAPI request lifecycle
* Separation of concerns (Routes vs Services)
* Dependency Injection (`Depends`)
* ORM vs Database interaction
* JWT Authentication basics
* Alembic migration workflow

---

## 📂 Project Structure

```
src/
 ├── main.py          # Entry point
 ├── config.py        # Settings & environment variables
 ├── db/
 │    ├── database.py # DB connection
 │    
 │
 ├── books/
 |    ├── models.py   # ORM models
 │    ├── routes.py   # API endpoints
 │    ├── service.py  # Business logic
 │    ├── schemas.py  # Pydantic models
 │
 ├── auth/ (in progress)
 │    ├── routes.py
 │    ├── service.py
 │    ├── schemas.py
```

---

## 🔐 Authentication Flow (Current)

```
User Signup → Store hashed password
User Login → Verify password → Generate JWT token
```

---

## ⚙️ Tech Stack

* FastAPI
* PostgreSQL
* SQLAlchemy / SQLModel
* Alembic
* Passlib (Password Hashing)
* PyJWT (Authentication)

---

## 🧪 How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn src.main:app --reload
```

---

## 🔄 Database Migration

```bash
# Create migration
alembic revision --autogenerate -m "message"

# Apply migration
alembic upgrade head
```

---

## 📌 Next Steps

* [ ] Complete HTTP Bearer Authentication
* [ ] Get current authenticated user
* [ ] Protect routes
* [ ] Add role-based access (later)
* [ ] Improve error handling

---

## 💡 Learning Note

This project is built step-by-step with a focus on:

* Deep understanding
* Writing code without copying
* Building production-ready backend skills

---

## 👨‍💻 Author

Vishwam Vaghasiya
