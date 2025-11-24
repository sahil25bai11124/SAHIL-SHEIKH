from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date, timedelta
from flask_mail import Mail, Message
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///habits.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Gmail SMTP server configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'  # Replace with your actual Gmail email address
app.config['MAIL_PASSWORD'] = 'your-email-password'  # Replace with your actual Gmail password or app-specific password
mail = Mail(app)

def send_reminder_email(user, habit):
    msg = Message('Habit Reminder', sender="your-email@gmail.com", recipients=[user.username])
    msg.body = f"Don't forget to complete your habit: {habit.name}"
    mail.send(msg)

scheduler = BackgroundScheduler()

def schedule_reminders():
    users = User.query.all()
    for user in users:
        habits = Habit.query.filter_by(user_id=user.id, completed=False).all()
        for habit in habits:
            send_reminder_email(user, habit)
scheduler.add_job(func=schedule_reminders, trigger="interval", hours=24)
scheduler.start()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    streak = db.Column(db.Integer, default=0)
    last_completed = db.Column(db.Date, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.String(100), nullable=True)

    def update_streak(self):
        if self.completed:
            if self.last_completed == date.today() - timedelta(days=1):
                self.streak += 1
            else:
                self.streak = 1
            self.last_completed = date.today()
        else:
            self.streak = 0

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Login unsuccessful. Please check your username and password.', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    habits = Habit.query.filter_by(user_id=current_user.id).all()
    dates = [(date.today() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
    completions = [habit.streak for habit in habits]
    return render_template('index.html', habits=habits, dates=dates, completions=completions)

@app.route('/add', methods=['POST'])
@login_required
def add_habit():
    habit_name = request.form.get('habit')
    category = request.form.get('category')
    if habit_name:
        new_habit = Habit(name=habit_name, user_id=current_user.id, category=category)
        db.session.add(new_habit)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/complete/<int:habit_id>')
@login_required
def complete_habit(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    if habit.user_id != current_user.id:
        abort(403)
    habit.completed = True
    habit.update_streak()
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/test_reminders')
def test_reminders():
    schedule_reminders()
    return 'Reminders sent!'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
