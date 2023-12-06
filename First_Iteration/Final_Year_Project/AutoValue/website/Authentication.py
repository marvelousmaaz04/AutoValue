from flask import Blueprint, flash,render_template,request,jsonify,redirect,url_for
from .Models import User
from . import db
from .Views import views

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
            
            return redirect(url_for("views.home")) # var name.func name
    return render_template("login.html")

@auth.route("/logout",methods=["GET"])
def logout():
    return ("logout")

@auth.route("/sign-up",methods=["GET","POST"])
def sign_up():
    if request.method == "POST":
        
        full_name = request.form.get("fullName")
        email = request.form.get("email")
        password = request.form.get("password")
        cpassword = request.form.get("cpassword")

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already in use.",category="error")
        elif len(full_name) < 5:
            flash("Full Name should be atleast 5 characters.",category="error")
        elif len(email) < 5:
            flash("Email should be atleast 5 characters.",category="error")
        elif len(password) < 4:
            flash("Password should be atleast 4 characters.",category="error")
        elif password != cpassword:
            flash("Both the passwords should match.",category="error")
        else:
            # create account
            new_user = User(full_name=full_name,email=email,password=password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("auth.login"))
    return render_template("signup.html")