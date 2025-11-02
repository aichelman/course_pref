import os
import csv
import random
import requests
from urllib.parse import quote_plus, urlparse, urlunparse
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

app = Flask(__name__)

def fix_database_url(url):
    """Fix database URL to handle special characters in password"""
    if not url:
        return None

    # Fix postgres:// to postgresql://
    if url.startswith('postgres://'):
        url = url.replace('postgres://', 'postgresql://', 1)

    # Parse the URL to handle special characters properly
    try:
        # Extract components manually for better control
        # Format: postgresql://user:password@host:port/database
        if '@' in url and '://' in url:
            scheme_and_auth = url.split('@')[0]
            host_and_rest = url.split('@')[1]

            scheme = scheme_and_auth.split('://')[0]
            auth = scheme_and_auth.split('://')[1]

            if ':' in auth:
                user, password = auth.split(':', 1)

                # Check if password is already URL-encoded
                # If it contains %XX patterns, assume it's already encoded
                import re
                is_already_encoded = bool(re.search(r'%[0-9A-Fa-f]{2}', password))

                if not is_already_encoded:
                    # URL-encode the password to handle special characters
                    encoded_password = quote_plus(password)
                else:
                    # Already encoded, use as-is
                    encoded_password = password

                # Reconstruct the URL with encoded password
                url = f"{scheme}://{user}:{encoded_password}@{host_and_rest}"
    except Exception as e:
        print(f"Warning: Could not parse database URL: {e}")
        # Return original URL if parsing fails
        pass

    # Add SSL mode if not present
    if '?' not in url:
        url += '?sslmode=require'

    return url

# Database configuration: Use PostgreSQL if DATABASE_URL is set, otherwise SQLite
database_url = os.environ.get('DATABASE_URL')

if database_url:
    # PostgreSQL - production with Supabase
    database_url = fix_database_url(database_url)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_size': 10,
        'max_overflow': 20,
        'connect_args': {
            'connect_timeout': 10,
            'keepalives': 1,
            'keepalives_idle': 30,
            'keepalives_interval': 10,
            'keepalives_count': 5,
        }
    }
else:
    # SQLite - local development
    db_dir = 'instance'
    os.makedirs(db_dir, exist_ok=True)
    db_path = os.path.join(db_dir, 'courses.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Session configuration - extend session lifetime
app.config['PERMANENT_SESSION_LIFETIME'] = 2592000  # 30 days in seconds
# Note: SESSION_COOKIE_SECURE disabled because Render uses reverse proxy
# The app runs on HTTP internally even though accessed via HTTPS externally
# Setting this to True can cause session/cookie issues with reverse proxies
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['REMEMBER_COOKIE_DURATION'] = 2592000  # 30 days for remember me

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

with app.app_context():
    db.create_all()

CSV_FILE = 'courses.csv'

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref='courses')

class Rating(db.Model):
    __tablename__ = 'rating'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    rating = db.Column(db.Float, default=1200)

    user = db.relationship('User', backref='ratings')
    course = db.relationship('Course', backref='ratings')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

@app.route('/')
@login_required
def index():
    return render_template('index.html', username=current_user.username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            # Clear any existing session data to prevent session fixation
            session.clear()
            session.permanent = True  # Make session last for PERMANENT_SESSION_LIFETIME
            login_user(user, remember=True)
            return jsonify({"status": "success"})
        return jsonify({"status": "error", "message": "Invalid username or password"}), 401

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')

        if User.query.filter_by(username=username).first():
            return jsonify({"status": "error", "message": "Username already exists"}), 400

        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        # Clear any existing session data to prevent session fixation
        session.clear()
        session.permanent = True  # Make session last for PERMANENT_SESSION_LIFETIME
        login_user(user, remember=True)
        return jsonify({"status": "success"})

    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()  # Clear all session data
    return redirect(url_for('login'))

@app.route('/pair')
@login_required
def pair():
    user_courses = Course.query.filter_by(user_id=current_user.id).all()
    if len(user_courses) < 2:
        return jsonify({"error": "Need at least 2 courses to compare"}), 400

    courses = random.sample(user_courses, 2)
    return jsonify({"course1": courses[0].name, "course2": courses[1].name})

@app.route('/vote', methods=['POST'])
@login_required
def vote():
    data = request.json
    winner = data['winner']
    loser = data['loser']
    update_ratings(current_user, winner, loser)
    return jsonify({"status": "success"})

@app.route('/rankings')
@login_required
def rankings():
    ratings = Rating.query.filter_by(user_id=current_user.id).join(Course).order_by(Rating.rating.desc()).all()
    ranked = [{"name": r.course.name, "rating": round(r.rating)} for r in ratings]
    return jsonify(ranked)

@app.route('/search_courses', methods=['GET'])
@login_required
def search_courses():
    query = request.args.get('query')

    # Use GolfCourseAPI for better golf-specific results
    api_key = os.environ.get('GOLF_COURSE_API_KEY')
    if not api_key:
        return jsonify({"error": "Golf Course API key not configured"}), 500

    url = "https://api.golfcourseapi.com/v1/search"
    params = {"search_query": query}
    headers = {
        "Authorization": f"Key {api_key}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Parse GolfCourseAPI response format
        results = []
        courses = data.get('courses', [])
        for course in courses[:10]:  # Limit to 10 results
            # Try to get name from various fields
            name = course.get('course_name') or course.get('club_name') or course.get('name', '')

            # Build address from location object
            location = course.get('location', {})
            address_parts = []
            if location.get('city'):
                address_parts.append(location.get('city'))
            if location.get('state'):
                address_parts.append(location.get('state'))
            if location.get('country'):
                address_parts.append(location.get('country'))

            address = ", ".join(address_parts) if address_parts else "Location not available"

            if name:  # Only add if we have a name
                results.append({"name": name, "address": address})

        return jsonify(results)

    except requests.exceptions.RequestException as e:
        print(f"Golf Course API error: {e}")
        return jsonify({"error": "Failed to search golf courses"}), 500

@app.route('/add_course', methods=['POST'])
@login_required
def add_course():
    course_name = request.json['name']

    # Check if user already has this course
    existing_course = Course.query.filter_by(name=course_name, user_id=current_user.id).first()
    if existing_course:
        return jsonify({"status": "already_exists", "course": course_name}), 400

    # Add course to database
    new_course = Course(name=course_name, user_id=current_user.id)
    db.session.add(new_course)
    db.session.commit()

    # Create rating entry for this course
    rating = Rating(user_id=current_user.id, course_id=new_course.id, rating=1200)
    db.session.add(rating)
    db.session.commit()

    return jsonify({"status": "added", "course": course_name})

@app.route('/upload_csv', methods=['POST'])
@login_required
def upload_csv():
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"status": "error", "message": "No file selected"}), 400

    if not file.filename.endswith('.csv'):
        return jsonify({"status": "error", "message": "File must be a CSV"}), 400

    # Read CSV file
    stream = file.stream.read().decode("utf-8")
    csv_input = csv.reader(stream.splitlines())

    added_count = 0
    for row in csv_input:
        if not row or not row[0].strip():
            continue

        course_name = row[0].strip()

        # Check if user already has this course
        existing_course = Course.query.filter_by(name=course_name, user_id=current_user.id).first()
        if not existing_course:
            new_course = Course(name=course_name, user_id=current_user.id)
            db.session.add(new_course)
            db.session.commit()

            # Create rating entry
            rating = Rating(user_id=current_user.id, course_id=new_course.id, rating=1200)
            db.session.add(rating)
            added_count += 1

    db.session.commit()
    return jsonify({"status": "success", "added": added_count})

def update_ratings(user, winner_name, loser_name, k=32):
    winner_course = Course.query.filter_by(name=winner_name, user_id=user.id).first()
    loser_course = Course.query.filter_by(name=loser_name, user_id=user.id).first()

    winner_rating = Rating.query.filter_by(user_id=user.id, course_id=winner_course.id).first()
    loser_rating = Rating.query.filter_by(user_id=user.id, course_id=loser_course.id).first()

    E_winner = 1 / (1 + 10 ** ((loser_rating.rating - winner_rating.rating) / 400))
    E_loser = 1 - E_winner

    winner_rating.rating += k * (1 - E_winner)
    loser_rating.rating += k * (0 - E_loser)

    db.session.commit()


if __name__ == '__main__':
    # Use environment variable to determine if we're in production
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug_mode, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
