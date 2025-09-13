# Django Ninja + PostgreSQL API

This project uses Django Ninja for API infrastructure and PostgreSQL as the database. It includes a Trip model with a name and a related Step model (many Steps per Trip).

## Setup Instructions

1. Install dependencies:
   ```zsh
   pip install django django-ninja psycopg2-binary
   ```
2. Configure PostgreSQL connection in `settings.py`.
3. Run migrations:
   ```zsh
   python manage.py migrate
   ```
4. Start the development server:
   ```zsh
   python manage.py runserver
   ```

## Models
- **Trip**: Has a `name` field and a one-to-many relationship with Step.
- **Step**: Belongs to a Trip.

## API
- Endpoints for Trip and Step management using Django Ninja.
