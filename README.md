# Habit Tracker

Habit Tracker is a web application that helps users track their daily habits. Users can register, log in, add habits, mark them as completed, and receive daily email reminders to complete their habits.

## Features

- User registration and login
- Add, view, and complete habits
- Track habit streaks
- Categorize habits
- Toggle dark mode
- Receive daily email reminders

## Technologies Used

- Flask (Python web framework)
- Flask-SQLAlchemy (ORM for database management)
- Flask-Login (User session management)
- Flask-Mail (Sending email reminders)
- APScheduler (Scheduling tasks)
- Bootstrap (CSS framework for styling)
- Chart.js (JavaScript library for charts)

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/habit-tracker.git
    cd habit-tracker
    ```

2. **Create a virtual environment:**

    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment:**

    - On Windows:

        ```bash
        venv\Scripts\activate
        ```

    - On macOS/Linux:

        ```bash
        source venv/bin/activate
        ```

4. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

5. **Set up the database:**

    ```bash
    flask db init
    flask db migrate -m "Initial migration."
    flask db upgrade
    ```

6. **Configure environment variables:**

    Create a `.env` file in the root directory and add the following:

    ```env
    FLASK_APP=app.py
    FLASK_ENV=development
    SECRET_KEY=your_secret_key
    SQLALCHEMY_DATABASE_URI=sqlite:///habits.db
    MAIL_SERVER=smtp.gmail.com
    MAIL_PORT=587
    MAIL_USE_TLS=True
    MAIL_USERNAME=your-email@gmail.com
    MAIL_PASSWORD=your-email-password
    ```

    Replace `your-email@gmail.com` and `your-email-password` with your actual Gmail email address and password.

## Usage

1. **Run the application:**

    ```bash
    flask run
    ```

2. **Open the application in your web browser:**

    Navigate to `http://127.0.0.1:5000/` in your web browser.

3. **Register a new user:**

    - Go to the registration page (`http://127.0.0.1:5000/register`) and create a new account.

4. **Log in:**

    - Log in with your newly created account (`http://127.0.0.1:5000/login`).

5. **Add and manage habits:**

    - Add new habits, mark them as completed, and track your progress.


