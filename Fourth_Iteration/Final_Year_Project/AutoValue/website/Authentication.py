import random
import time
from flask import Blueprint, flash,render_template,request,jsonify,redirect,url_for, make_response, session

from .Models import User
from . import db
from .Views import views
from flask_login import login_user,login_required,logout_user, current_user
from email.message import EmailMessage
import ssl
import smtplib
from datetime import datetime, timedelta

auth = Blueprint("auth",__name__)

@auth.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        
        
        email = request.form.get("email")
        password = request.form.get("password")
        

        user = User.query.filter_by(email=email).first()
        if not user:
            flash("Email does not exist.",category="error")
        elif password != user.password:
            flash("Incorrect Password, try again.",category="error")
        else:
            login_user(user, remember=True)
            return redirect(url_for("views.landing_page")) # var name.func name
    return render_template("login.html")


@auth.route("/logout",methods=["POST","GET"])
@login_required
def logout():
    logout_user()
    # Create a response object
    response = make_response(redirect(url_for('auth.login')))

    # Set Cache-Control headers to prevent caching
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response 

otp_storage = {}

@auth.route("/sign-up",methods=["GET","POST"])
def sign_up():
    if request.method == "POST":
        print('post req sent')
        full_name = request.form.get("fullName")
        email = request.form.get("email")
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already in use.",category="error")
            
        elif len(full_name) <= 5:
            flash("Full Name should be more than 5 characters.",category="error")
            
        elif len(email) <= 5:
            flash("Invalid email address",category="error")
            
            
        else:
            # create account
            # new_user = User(full_name=full_name,email=email,password=password)
            # db.session.add(new_user)
            # db.session.commit()
            email_sender = 'autovaluesup@gmail.com'
            email_password = 'qoti aruq tswy zzlw' # better to use environment var
            email_receiver = email
            
            subject = 'OTP FOR EMAIL VERIFICATION'
            otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            otp_storage[email] = {'otp': otp, 'timestamp': time.time()}
            # link = "http://localhost:5000/reset-password"
            body = f"OTP: {otp}. OTP expires in 5 minutes."
            email_message = EmailMessage()
            email_message['From'] = 'AutoValue Support' # this will be displayed to the user
            email_message['To'] = email_receiver
            email_message['Subject'] = subject
            email_message.set_content(body)

            context = ssl.create_default_context()

            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email_receiver, email_message.as_string())
                session['email'] = email
                session['fullName'] = full_name
            flash("Email sent successfully! Enter the OTP provided.", category="success")
            return redirect(url_for("auth.verify_email"))
    return render_template("signup.html")


@auth.route("/verify-email",methods=['GET','POST'])
def verify_email():
    email = session .get('email')
    if request.method == 'POST':
        entered_otp = request.form.get('otp')
        # Retrieve OTP and its creation time from storage
        stored_otp_data = otp_storage.get(email)
        if stored_otp_data and stored_otp_data['otp'] == entered_otp:
            # Check if OTP is still valid (within 5 minutes)
            if time.time() - stored_otp_data['timestamp'] <= 300:  # 300 seconds = 5 minutes
                # OTP verification successful, proceed to password setup
                session['email'] = email  # Store email in session for password setup
                flash("Email has been verified! Set your Password", category="success")
                return redirect('/set-password')
            else:
                # OTP has expired, display error message
                flash("OTP has expired.", category="error")
                return render_template('verify_email.html')
        else:
            # Invalid OTP, display error message
            flash("Invalid OTP.", category="error")
            return render_template('verify_email.html')
    return render_template('verify_email.html', email=email)


@auth.route("/set-password",methods=['GET','POST'])
def set_password():
    if request.method == "POST":
        full_name = session.get("fullName")
        email = session.get("email")
        password = request.form.get("password")
        cpassword = request.form.get("cpassword")

        if password != cpassword:
            flash("Passwords do not match.",category="error")
        else:
            # create account
            new_user = User(full_name=full_name,email=email,password=password)
            db.session.add(new_user)
            db.session.commit()
            flash("Successfully Signed Up! You can now Log in.", category="success")
            return redirect(url_for("auth.login"))

    return render_template("set_password.html")


email_sender = 'autovaluesup@gmail.com'
email_password = 'qoti aruq tswy zzlw' # better to use environment var
reset_user_email = ""
@auth.route("/forgot-password",methods=['GET','POST'])
def forgot_password():
    global reset_user_email
    if request.method == "POST":
        
        
        email = request.form.get("email")
        

        user = User.query.filter_by(email=email).first()
        if not user:
            flash("Email does not exist.",category="error")
        else:
            user.generate_reset_token()
            db.session.commit()
            email_receiver = email
            
            reset_user_email = email
            subject = 'Password Reset Request'
            reset_link = url_for('auth.reset_password', token=user.reset_token, _external=True)
            # link = "http://localhost:5000/reset-password"
            body = f"Click on the link to reset your password. Link is valid for 5 minutes.\n\nPassword reset link: {reset_link}"
            email_message = EmailMessage()
            email_message['From'] = 'AutoValue Support' # this will be displayed to the user
            email_message['To'] = email_receiver
            email_message['Subject'] = subject
            email_message.set_content(body)

            context = ssl.create_default_context()

            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email_receiver, email_message.as_string())
            flash('Email sent successfully. Check your inbox.', category="success")
    return render_template("forgot_password_copy.html")

@auth.route('/reset-password',methods=['GET','POST'])
def reset_password():
    if request.method == "POST":
        token = request.args.get('token')
        new_password = request.form.get('password')
        confirm_password = request.form.get("cpassword")
        user = User.query.filter_by(email=reset_user_email).first()
        if (user and token == user.reset_token and user.reset_token_expiration and user.reset_token_expiration > datetime.utcnow() and new_password == confirm_password):
            
            user.reset_token = None
            user.reset_token_expiration = None
            user.password = new_password
            db.session.commit()
            flash("Password reset successfully.", category="reset-success")
        else:
            flash('Token has been expired.', category='reset-error')
    return render_template("reset_password.html")