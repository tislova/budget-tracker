# Budget Tracker

A full-stack Flask web application for tracking personal income and expenses, 
with monthly summaries, category breakdowns, and interactive pie chart 
visualization. Each user has a private account with their own transaction 
history.

[Watch the demo video](https://drive.google.com/file/d/1u4Xi7LyFolyvbTISa3t1ZhibPslgZPAz/view?usp=sharing)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/sqlalchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Bootstrap](https://img.shields.io/badge/bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)
![Chart.js](https://img.shields.io/badge/chart.js-FF6384?style=for-the-badge&logo=chart.js&logoColor=white)

## Overview

Users register, log in securely, and add income or expense transactions 
categorized across 11 predefined categories (Housing, Transportation, Food, 
etc.). The home dashboard shows real-time monthly totals and a pie chart 
breaking down expenses by category. Each user's data is fully isolated 
through database-level foreign key relationships.

## Features

- **Secure authentication** — Email and password with pbkdf2:sha256 hashing (Werkzeug)
- **User-scoped data** — Foreign key relationships ensure users only see their own transactions
- **Income and expense tracking** — Add transactions with amount, month, and category
- **Monthly dashboard** — Select any month to see total earned, total spent, and budget remaining
- **Interactive pie chart** — Expenses by category, regenerated dynamically when the user changes month (Chart.js + AJAX)
- **Transaction history** — Full chronological list with delete functionality
- **Server-side validation** — Empty fields, invalid amounts, password length, duplicate emails all caught with flash messages
- **Responsive design** — Bootstrap 4 layout works across desktop, tablet, mobile

## Tech Stack

- **Backend:** Python, Flask, Flask-Login, Flask-SQLAlchemy
- **Database:** SQLite (via SQLAlchemy ORM)
- **Authentication:** Werkzeug security (`generate_password_hash`, `check_password_hash`)
- **Frontend:** HTML, Jinja2 templating, Bootstrap 4, custom CSS
- **Visualization:** Chart.js
- **AJAX:** Native `fetch` API for dashboard updates

## Architecture

The app uses a professional Flask structure:

- **Application factory pattern** — `create_app()` function in `website/__init__.py` for initialization and testability
- **Blueprint architecture** — Routes split into `views` (main app) and `auth` (login/signup/logout) blueprints
- **ORM models** — `User` and `Transaction` defined with SQLAlchemy in `models.py`, with foreign key relationship
- **Decorator-based access control** — Routes protected with `@login_required` from Flask-Login
- **Server-rendered + AJAX hybrid** — Pages rendered with Jinja2 templates, dashboard updates use JSON endpoints
- **Environment-based secrets** — `SECRET_KEY` loaded from environment variable with a development fallback

## Project Structure

```plaintext
budget-tracker/
├── website/
│   ├── __init__.py        #App factory, blueprint registration, DB setup, login manager
│   ├── auth.py            #Login, signup, logout routes (auth blueprint)
│   ├── views.py           #Home, expenses, income, history routes (views blueprint)
│   ├── models.py          #User and Transaction SQLAlchemy models
│   ├── static/
│   │   └── styles.css     #Custom theme on top of Bootstrap
│   └── templates/
│       ├── index.html     #Base template with navbar, flash messages, Chart.js CDN
│       ├── login.html     #Landing page with Login / Sign up buttons
│       ├── login_page.html
│       ├── signup.html
│       ├── home.html      #Dashboard with month selector and pie chart
│       ├── expenses.html  #Form to add expense transactions
│       ├── income.html    #Form to add income transactions
│       └── history.html   #Chronological transaction list with delete
├── main.py                #Entry point
└── database.db            #SQLite database (auto-generated on first run)
```

## Running the App

**Prerequisites:** Python 3.8+

```bash
#Clone the repository
git clone https://github.com/tislova/budget-tracker.git
cd budget-tracker

#Install dependencies
pip install flask flask-sqlalchemy flask-login werkzeug

#Run the app
python main.py
```

The app will be available at `http://localhost:5000`. The SQLite database 
is created automatically on first launch.

**For production deployments:** set the `SECRET_KEY` environment variable to 
a secure random value before running:

```bash
export SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
python main.py
```

## Key Code Decisions

- **Application factory** — Using `create_app()` instead of a top-level `app = Flask(__name__)` makes the app testable and supports multiple configurations (dev/prod).
- **Blueprints** — Splitting auth and main routes into separate modules keeps `views.py` focused on business logic.
- **User-scoped queries** — Every transaction query filters by `user_id=current_user.id`, ensuring data isolation between users.
- **JSON endpoint for dashboard** — The `/` POST handler returns JSON instead of rendering HTML, enabling the dynamic pie chart updates without page reloads.
- **Environment-based secrets** — `SECRET_KEY` is pulled from `os.environ` with a development fallback, so the app runs locally without setup while still supporting secure production deployment.

## Skills Demonstrated

- **Full-stack Flask development** — Routes, templates, forms, database integration
- **Authentication and security** — Password hashing, session management, login-required decorators
- **Secrets management** — Environment-variable configuration with safe development fallback
- **Relational database design** — User and Transaction tables with foreign key relationship
- **ORM usage** — SQLAlchemy models, queries, filtering, ordering
- **Blueprint-based modularization** — Clean separation of concerns
- **Application factory pattern** — Professional Flask project structure
- **Server-side validation** — Input checking with user-friendly flash messages
- **AJAX with fetch API** — Dynamic dashboard updates without page reload
- **Data visualization** — Chart.js pie chart with dynamic data binding
- **Responsive design** — Bootstrap 4, custom CSS

## What I'd Add With More Time

- Add a `requirements.txt` for reproducible installs
- Export transactions to CSV
- Add budget targets per category with overspend warnings
- Multi-currency support
- Recurring transactions (rent, subscriptions, salary)
- Year-over-year comparison view
- Unit tests for the helper logic and integration tests for auth flow
- Migrate to PostgreSQL for production deployment
