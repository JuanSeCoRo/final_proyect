# BEGIN app.py
from flask import Flask, render_template, request, redirect, url_for
import requests
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from models import db, User, Result

# Flask application setup
app = Flask(__name__)
app.secret_key = 'supersecretkey'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecoimpact.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize the database
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def index():
    return render_template('index.html')

# Route for the calculator page
# This route renders the calculator page where users can input their data
@app.route('/calculator')
@login_required
def calculator():
    return render_template('calculator.html')

# Route to handle the form submission and calculate the carbon footprint
# This route processes the form data submitted from the calculator page
@app.route('/result', methods=['POST'])
@login_required
def result():
    # Get the form data
    transport = int(request.form.get('transport'))
    meat = int(request.form.get('meat'))
    energy = int(request.form.get('energy'))

    co2_transport = transport * 2
    co2_meat = meat * 5
    co2_energy = energy * 0.5
    total = co2_transport + co2_meat + co2_energy

    # Determine the message based on the total carbon footprint
    message = (
        "Your footprint is above the average. Try reducing car use and meat consumption."
        if total > 5000 else
        "You're doing okay, but there's still room to improve. Maybe switch to LEDs or bike more."
        if total > 2500 else
        "Great job! Your carbon footprint is lower than average. Keep up the green habits."
    )

    # Save the result to the database
    result_data = Result(
        user_id=current_user.id,
        date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        transport=co2_transport,
        meat=co2_meat,
        energy=co2_energy,
        total=total
    )
    db.session.add(result_data)
    db.session.commit()

    # Render the result template with the calculated data
    return render_template('result.html', total=round(total, 2), message=message, data={
        'transport': co2_transport,
        'meat': co2_meat,
        'energy': co2_energy
    })

# Route for viewing history and clearing it
# This route fetches the user's results from the database and displays them
@app.route('/history')
@login_required
def history():
    results = Result.query.filter_by(user_id=current_user.id).order_by(Result.id.desc()).all()
    return render_template('history.html', results=results)

# Route to clear the user's history
@app.route('/clear_history', methods=['POST'])
@login_required
def clear_history():
    Result.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    return redirect(url_for('history'))

# Route for the climate page
# This route fetches current weather data from an API and displays it
@app.route('/climate', methods=['GET', 'POST'])
@login_required
def climate():
    weather_data = None
    if request.method == 'POST':
        city = request.form.get('city')
        # Fetch weather data for the specified city
        try:
            url = f"https://api.open-meteo.com/v1/forecast?latitude=4.61&longitude=-74.08&current_weather=true"
            r = requests.get(url)
            data = r.json()['current_weather']
            weather_data = {
                'temperature': data['temperature'],
                'windspeed': data['windspeed'],
                'weathercode': data['weathercode'],
                'city': city
            }
        except:
            weather_data = {'error': 'Could not fetch data'}
    return render_template('climate.html', weather=weather_data)

# User authentication routes
# This route allows users to log in to their account
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        # Check if user exists and password matches
        if not user:
            error = "Account does not exist."
        elif user.password != password:
            error = "Incorrect username or password."
        else:
            login_user(user)
            return redirect(url_for('index'))

    return render_template('login.html', error=error)

# Route for user registration
# This route allows new users to register an account
@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            error = "Username already exists!"
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))

    return render_template('register.html', error=error)

# Route for user logout
# This route logs out the user and redirects to the index page
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Route for user settings (change password)
# Login required to access settings
@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    error = None
    success = None

    if request.method == 'POST' and 'old_password' in request.form:
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')

        # Check old password is correct
        if current_user.password != old_password:
            error = "Incorrect current password."
        elif len(new_password) < 6:
            error = "New password must be at least 6 characters long."
        else:
            # Save new password
            user = User.query.get(current_user.id)
            user.password = new_password
            db.session.commit()
            success = "Your password has been changed."

    return render_template('settings.html', error=error, success=success)

# Route to delete user account
@app.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    # Delete user results first (foreign key constraint)
    Result.query.filter_by(user_id=current_user.id).delete()
    # Delete the user account
    user = User.query.get(current_user.id)
    db.session.delete(user)
    db.session.commit()
    logout_user()
    return redirect(url_for('index'))

# Route to change user password
@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    error = None
    success = None

    if request.method == 'POST':
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')

        if current_user.password != old_password:
            error = "Incorrect current password."
        elif len(new_password) < 6:
            error = "New password must be at least 6 characters long."
        else:
            user = User.query.get(current_user.id)
            user.password = new_password
            db.session.commit()
            success = "Your password has been changed."

    return render_template('change_password.html', error=error, success=success)

# Route to handle 404 errors
if __name__ == '__main__':
    app.run(debug=True)
