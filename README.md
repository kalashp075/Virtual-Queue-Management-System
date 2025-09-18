# VQMS - Service Queue Management System

This project is a web-based Service Queue Management System built with Django. It allows users to sign up, log in, and manage their service requests efficiently. The system features user authentication, service selection, profile management, and queue tracking. The frontend uses HTML templates and custom CSS for a user-friendly interface.

## Features

- User registration and login
- Service selection and detail view
- Profile management
- Queue tracking for services
- Responsive UI with custom styles

## Structure

- `myapp/`: Main Django app with models, views, templates, and static files
- `myproject/`: Django project configuration and settings
- `db.sqlite3`: SQLite database for development

## Getting Started

1. Install dependencies:  
   `pip install django`
2. Run migrations:  
   `python manage.py migrate`
3. Start the server:  
   `python manage.py runserver`
