from flask import Blueprint,render_template,request

spinny_routes = Blueprint("spinny_routes",__name__)

@spinny_routes.route("/spinny/mumbai",methods=["GET"])
def spinny_mumbai():
    return ("<h1>Spinny</h1>")

@spinny_routes.route("/spinny/delhi",methods=["GET"])
def spinny_delhi():
    pass

@spinny_routes.route("/spinny/hyderabad",methods=["GET"])
def spinny_hyderabad():
    pass

@spinny_routes.route("/spinny/bangalore",methods=["GET"])
def spinny_bangalore():
    pass

@spinny_routes.route("/spinny/pune",methods=["GET"])
def spinny_pune():
    pass