import os

from click import DateTime
from flask import Flask, render_template, request, redirect, url_for, flash, session
from numpy.f2py.rules import generationtime
from sqlalchemy import or_
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from dotenv import load_dotenv

from database.models import UserLogin, engine, UserContent
from services.image_generator import StableDiffusionClient
from services.file_manager import add_image
from services.notification_service import EmailNotificationSender

load_dotenv()

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this in production

Session = sessionmaker(bind=engine, autoflush=True)
db_session = Session()



@app.route('/', methods=['GET', 'POST'])
def blank():
    return redirect(url_for('login'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_or_email = request.form.get('username')
        username_or_email = username_or_email.lower()
        password = request.form.get('password')

        user = db_session.query(UserLogin).filter(
            or_(
                UserLogin.username == username_or_email,
                UserLogin.email == username_or_email
            )
        ).first()


        if user and check_password_hash(user.password, password):
            session['user_id'] = user.user_id
            user.last_login = datetime.datetime.now()
            db_session.commit()  # Commit after updating last login
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')  # No need to specify templates folder explicitly



@app.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')

    if not user_id:
        flash('Please log in to access the dashboard.', 'warning')
        print("No User ID")
        return redirect(url_for('login'))

    user = db_session.query(UserLogin).filter_by(user_id=user_id).first()

    if user:
        return render_template('dashboard.html', user=user)
    else:
        flash('User not found.', 'danger')
        return redirect(url_for('login'))



@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    print("Logged Out")
    return redirect(url_for('login'))



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email').lower()
        username = request.form.get('username').lower()
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        existing_user_username = db_session.query(UserLogin).filter_by(username=username).first()
        existing_user_email = db_session.query(UserLogin).filter_by(email=email).first()

        if existing_user_username:
            flash('Username already exists.', 'danger')
            return redirect(url_for('register'))
        if existing_user_email:
            flash('Email already exists.', 'danger')
            return redirect(url_for('register'))

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('register'))

        new_user = UserLogin(
            user_id=username,
            username=username,
            email=email,
            password=generate_password_hash(password),
            created_at=datetime.datetime.now(),
            last_login=None
        )

        db_session.add(new_user)
        db_session.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')  # No need to specify templates folder explicitly


@app.route('/generate', methods=['GET', 'POST'])
def generate():
    if request.method == 'POST':
        print("Post Request sent")
        description = request.form.get('image_input')
        generate_type = request.form.get('generate_type')
        print(generate_type)

        if not description:
            print('Please enter a description.')
            return redirect(url_for('generate'))

        if generate_type == 'image':
            print("Image being Produced")

            generation_time = datetime.datetime.now()

            new_content = UserContent(
                user_id=session['user_id'],
                prompt = description,
                paths_url = "",
                status = "Processing",
                generated_at = generation_time,
            )
            db_session.add(new_content)
            db_session.commit()

            user_email = db_session.query(UserLogin).filter(UserLogin.user_id == session['user_id']).first().email
            try:
                client = StableDiffusionClient(
                    token=os.getenv("HUGGING_FACE_TOKEN")
                )
                image = client.query(prompt=description)
                save_link = add_image(session['user_id'],image)
                if save_link:
                    existing_content = db_session.query(UserContent).filter_by(
                        user_id=session['user_id'],
                        prompt=description,
                        generated_at=generation_time
                    ).one()
                    existing_content.status = "Completed"
                    existing_content.paths_url = save_link
                    db_session.commit()
                    print(f"🔗 Image link: {save_link}")

                    print("📧 Sending email notification to the user...")
                    EmailNotificationSender().send_email(to_email=user_email, image_link=save_link)
            except Exception as e:
                print(f"Error during image generation or upload: {e}")
                existing_content = db_session.query(UserContent).filter_by(
                    user_id=session['user_id'],
                    prompt=description,
                    generated_at=generation_time
                ).one()
                existing_content.status = "Failed"
                db_session.commit()

        elif generate_type == 'video':
            print("This is currently under construction please use image only")

    return render_template('generate.html')  # Create this HTML template


if __name__ == '__main__':
    app.run(debug=True)
