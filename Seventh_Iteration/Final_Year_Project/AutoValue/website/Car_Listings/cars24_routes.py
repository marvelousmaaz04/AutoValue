from flask import Blueprint,render_template,request

cars24_routes = Blueprint("cars24_routes",__name__)

@cars24_routes.route("/cars24/mumbai",methods=["GET"])
def cars24_mumbai():
    return ("<h1>Cars24</h1>")

@cars24_routes.route("/cars24/delhi",methods=["GET"])
def cars24_delhi():
    pass

@cars24_routes.route("/cars24/hyderabad",methods=["GET"])
def cars24_hyderabad():
    pass

@cars24_routes.route("/cars24/bangalore",methods=["GET"])
def cars24_bangalore():
    pass

@cars24_routes.route("/cars24/pune",methods=["GET"])
def cars24_pune():
    pass