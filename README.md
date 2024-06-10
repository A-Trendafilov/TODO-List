# TODO List Web App.

A simple task management web application built using Flask, SQLite, and Bootstrap. Users can register, log in, create,
edit, delete, and mark tasks as completed. They can also update their profile information and change their password.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#setup-instructions)
- [Structure](#project-structure)
- [API Endpoints](#routes)
- [Screenshots](#Screenshots)

## Features

- User registration and login
- Task creation, editing, deletion, and completion
- Profile management with password change functionality
- Flash messages for user feedback
- Responsive design using Bootstrap

## Requirements

- Python 3.8+
- Flask
- Flask-Bootstrap
- Flask-Login
- Flask-SQLAlchemy
- python-dotenv
- Werkzeug

## Setup Instructions

1. **Clone the repository:**

    ```bash
    git clone https://github.com/A-Trendafilov/flask-task-manager.git
    cd flask-task-manager
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**

   Create a `.env` file in the root directory and add your secret key:

    ```plaintext
    SECRET_KEY=your_secret_key
    ```

5. **Initialize the database:**

   Uncomment the following lines in `app.py` to create the database on the first run:

    ```python
    # Uncomment on the 1st run to create the database.
    # with app.app_context():
    #     db.create_all()
    ```

   Run the application once to create the database:

    ```bash
    python app.py
    ```

   After the database is created, comment out the lines again to prevent reinitialization.

6. **Run the application:**

    ```bash
    python app.py
    ```

   The application will be available at `http://127.0.0.1:5000/`.

## Project Structure

- `main.py`: Main application file.
- `db_model.py`: Database models for `User` and `Task`.
- `forms.py`: Forms for registration, login, task management, profile editing, and password change.
- `templates/`: HTML templates for rendering pages.
- `static/`: Static files like CSS and JavaScript.
- `.env`: Environment variables.
- `requirements.txt`: List of dependencies.

## Routes

- `/`: Home page with login form.
- `/create-account`: Registration page.
- `/tasks`: View and create tasks (requires login).
- `/tasks/edit/<int:task_id>`: Edit a task (requires login).
- `/tasks/delete/<int:task_id>`: Delete a task (requires login).
- `/tasks/complete/<int:task_id>`: Mark a task as completed (requires login).
- `/tasks/completed`: View completed tasks (requires login).
- `/profile`: View user profile (requires login).
- `/profile/edit`: Edit user profile and change password (requires login).
- `/logout`: Log out the current user.

## Screenshots

<img alt="Screenshot 1" src="/screenshots/todo_1.png"/>

<img alt="Screenshot 2" src="/screenshots/todo_2.png"/>

<img alt="Screenshot 3" src="/screenshots/todo_3.png"/>