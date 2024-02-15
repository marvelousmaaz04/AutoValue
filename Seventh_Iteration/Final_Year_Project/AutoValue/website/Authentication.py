import random
import time
from flask import Blueprint, flash,render_template,request,jsonify,redirect,url_for, make_response, session
from werkzeug.security import generate_password_hash, check_password_hash
from .Models import Users, UserLogin
from .Models import Subscribers, ContactUs

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
        
        # query UserLogin model
        user = UserLogin.query.filter_by(email=email).first()
        if not user:
            flash("Email Address is not Registered.",category="error")
        elif not check_password_hash(user.password, password):
            flash("Incorrect Password, try again.",category="error")
        else:
            login_user(user, remember=True)
            session['user_id'] = user.id
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
        user = Users.query.filter_by(email=email).first()
        if user:
            flash("Email Address is already Registered.",category="error")
            
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
            email_password = 'eryj kyjp gotk vmvo' # better to use environment var
            email_receiver = email
            
            subject = 'OTP FOR EMAIL VERIFICATION'
            otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            otp_storage[email] = {'otp': otp, 'timestamp': time.time()}
         
            body = f"<b>OTP: {otp}</b>. <b>Your OTP expires in 5 minutes.</b>"
            email_message = EmailMessage()
            email_message['From'] = 'AutoValue Support' # this will be displayed to the user
            email_message['To'] = email_receiver
            email_message['Subject'] = subject
            email_message.set_content(body, subtype="html")

            context = ssl.create_default_context()

            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                
                context = ssl.create_default_context()
                # email_exists = verifier(email_receiver)
                
                smtp.sendmail(email_sender, email_receiver, email_message.as_string())
                session['email'] = email
                session['fullName'] = full_name
            
                flash("Enter the OTP provided in the Email. OTP expires in 5 minutes.", category="success")
                return redirect(url_for("auth.verify_email_otp"))
                
                
           
            
                    
    return render_template("signup.html")



@auth.route("/verify-email",methods=['GET','POST'])
def verify_email_otp():
    email = session.get('email')
    if request.method == 'POST':
        entered_otp = request.form.get('otp')
        # Retrieve OTP and its creation time from storage
        stored_otp_data = otp_storage.get(email)
        if stored_otp_data and stored_otp_data['otp'] == entered_otp:
            # Check if OTP is still valid (within 5 minutes)
            if time.time() - stored_otp_data['timestamp'] <= 300:  # 300 seconds = 5 minutes
                # OTP verification successful, proceed to password setup
                session['email'] = email  # Store email in session for password setup
                otp_storage.pop(email, None)
                
                flash("Email has been verified! Set your Password.", category="success")
                return redirect('/set-password')
            else:
                # OTP has expired, display error message
                otp_storage.pop(email, None)
                session.pop('email',None)
                flash("OTP has expired!", category="expire-error")
                return render_template('verify_email.html')
        else:
            # Invalid OTP, display error message
        
            flash("OTP entered is Invalid! Enter correct OTP.", category="invalid-error")
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
            hashed_password = generate_password_hash(password) # generate hash of password
            # create account
            new_user = Users(full_name=full_name,email=email,password=hashed_password)
            db.session.add(new_user)

            # Create account in UserLogin table
            new_user_login = UserLogin(email=email, password=hashed_password)
            db.session.add(new_user_login)

            db.session.commit()
            session.pop('email',None)
            flash("Successfully Signed Up! You can now Log in.", category="success")
            return redirect(url_for("auth.login"))

    return render_template("set_password.html")


email_sender = 'autovaluesup@gmail.com'
email_password = 'eryj kyjp gotk vmvo' # better to use environment var
reset_user_email = ""
@auth.route("/forgot-password",methods=['GET','POST'])
def forgot_password():
    global reset_user_email
    if request.method == "POST":
        
        
        email = request.form.get("email")
        

        user = Users.query.filter_by(email=email).first()
        if not user:
            flash("Email Address is not Registered.",category="error")
        else:
            user.generate_reset_token()
            db.session.commit()
            email_receiver = email
            
            reset_user_email = email
            subject = 'Password Reset Request'
            reset_link = url_for('auth.reset_password', token=user.reset_token, _external=True)
            # link = "http://localhost:5000/reset-password"
            body = f"<b>Click on the link to reset your password. Link is valid for 5 minutes.</b><br><br><b>Password reset link:</b> {reset_link}"
            email_message = EmailMessage()
            email_message['From'] = 'AutoValue Support' # this will be displayed to the user
            email_message['To'] = email_receiver
            email_message['Subject'] = subject
            email_message.set_content(body, subtype='HTML')

            context = ssl.create_default_context()

            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email_receiver, email_message.as_string())
            flash('Email sent successfully! Check your inbox.', category="success")
    return render_template("forgot_password.html")

@auth.route('/reset-password',methods=['GET','POST'])
def reset_password():
    if request.method == "POST":
        token = request.args.get('token')
        new_password = request.form.get('password')
        confirm_password = request.form.get("cpassword")
        user = Users.query.filter_by(email=reset_user_email).first()
        user_login = UserLogin.query.filter_by(email=reset_user_email).first()
        if (user and token == user.reset_token and user.reset_token_expiration and user.reset_token_expiration > datetime.utcnow() and new_password == confirm_password):
            
            hashed_new_password = generate_password_hash(new_password)

            user.reset_token = None
            user.reset_token_expiration = None

            user.password = hashed_new_password
            user_login.password = hashed_new_password

            db.session.commit()
            flash("Password reset successfully!", category="reset-success")
        else:
            user.reset_token = None
            user.reset_token_expiration = None
            flash('Token has been expired.', category='reset-error')
    return render_template("reset_password.html")

@auth.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form['email-input']
    user = Users.query.filter_by(email=email).first()
    user_id = ""
    if user:
        user_id = user.id
    # Check if the email already exists in the database
    
    if user and session['user_id'] == user.id:
        existing_subscriber = Subscribers.query.filter_by(email=email).first()
        if existing_subscriber:
            # Email already exists, return a message
            return jsonify({'message': 'You have already subscribed!'})
        
        # Add the email to the database
        else:
            subscriber = Subscribers(email=email)
            db.session.add(subscriber)
            db.session.commit()
            email_sender = 'autovaluesup@gmail.com'
            email_password = 'eryj kyjp gotk vmvo' # better to use environment var
            email_receiver = email
            
            subject = 'Welcome to AutoValue Weekly Newsletter'
            
            # link = "http://localhost:5000/reset-password"
            # Blog titles and links
            blog_titles = [
                ("Ferrari 499P Modificata unveiled", "https://www.autocarindia.com/car-news/ferrari-499p-modificata-unveiled-429704"),
                ("Lamborghini Huracan Sterrato Deliveries Commence in India; Price Starts at Rs 4.61 Crore", "https://www.autox.com/news/car-news/lamborghini-huracan-sterrato-deliveries-commence-in-india-price-starts-at-rs-461-crore-115047/"),
                ("FOSS Movement: Porsche Anchors Open Source in Software Strategy", "https://indianautosblog.com/foss-movement-porsche-anchors-open-source-in-software-strategy-p326119"),
                ("Mahindra Pending Orders At 2.86 Lakh – Scorpio 119k, Thar 76k, XUV700 70k", "https://www.rushlane.com/mahindra-pending-orders-at-2-86-lakh-scorpio-119k-thar-76k-xuv700-70k-12482080.html"),
                ("Mercedes Benz GLE facelift launched at Rs 96.4 lakh", "https://www.autocarindia.com/car-news/mercedes-benz-gle-facelift-launched-at-rs-964-lakh-429735"),
            ]

            # Constructing the HTML body with clickable links
            body = "<h2>Top Trends for this week:</h2>"
            body += "<h3><ol>"
            for title, link in blog_titles:
                body += f"<li><a href='{link}'>{title}</a></li>"
            body += "</ol></h3>"

            # Create EmailMessage object
            email_message = EmailMessage()
            email_message['From'] = 'AutoValue'  # This will be displayed to the user
            email_message['To'] = email_receiver
            email_message['Subject'] = subject
            email_message.add_alternative(body, subtype='html')  # Set the body as HTML content

            context = ssl.create_default_context()

            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                
                context = ssl.create_default_context()
                # email_exists = verifier(email_receiver)
                
                smtp.sendmail(email_sender, email_receiver, email_message.as_string())
            # Email added successfully, return a message
            return jsonify({'message': 'You have successfully subscribed!'})
    else:
        return jsonify({'message': 'Invalid Email Address!'})

email_sender = 'autovaluesup@gmail.com'
email_password = 'eryj kyjp gotk vmvo' # better to use environment var
    
@auth.route('/contact', methods=['POST'])
def contact():
    client_name = request.form['client-name']
    client_email = request.form['client-email']
    # client_phone = request.form['client-number']
    client_message = request.form['client-message']

    
    print(client_message)

    user = Users.query.filter_by(email=client_email).first()
    user_id = ""
    if user:
        user_id = user.id
    if user and session["user_id"] == user_id:
       
        contact = ContactUs(name=client_name, email=client_email, message=client_message)
        db.session.add(contact)
        db.session.commit()


        email_receiver = client_email
        
        # Process the form data as needed (e.g., send email, save to database)
        subject = 'Thanks for reaching out to AutoValue Support'
        body = f"""Dear {client_name},

            Thank you for reaching out to AutoValue Support. Your query is important to us, and we appreciate the opportunity to assist you.

            Our team is currently reviewing your message and will respond to you promptly. We strive to provide the highest level of service and will do our best to address your concerns or questions.

            In the meantime, if you have any urgent matters or additional information to share, please feel free to contact us directly at autovaluesup@gmail.com or 7977962360.

            Thank you for choosing AutoValue. We look forward to serving you.

            Best regards,
            AutoValue Support Team"""

            # Create EmailMessage object
        email_message = EmailMessage()
        email_message['From'] = 'AutoValue Support'  # This will be displayed to the user
        email_message['To'] = email_receiver
        email_message['Subject'] = subject
        email_message.set_content(body)  # Set the body as HTML content

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            
            context = ssl.create_default_context()
            # email_exists = verifier(email_receiver)
            
            smtp.sendmail(email_sender, email_receiver, email_message.as_string())
        
        # Return a response
        return jsonify({'message': 'Message sent successfully!'})
        
    else:
        return jsonify({'message': 'Invalid Email Address!'})