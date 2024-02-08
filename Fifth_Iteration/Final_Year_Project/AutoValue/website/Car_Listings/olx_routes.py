from flask import Blueprint,render_template,request

olx_routes = Blueprint("olx_routes",__name__)

@olx_routes.route("/olx/mumbai",methods=["GET"])
def olx_mumbai():
    return ("<h1>OLX</h1>")

@olx_routes.route("/olx/delhi",methods=["GET"])
def olx_delhi():
    pass

@olx_routes.route("/olx/hyderabad",methods=["GET"])
def olx_hyderabad():
    pass

@olx_routes.route("/olx/bangalore",methods=["GET"])
def olx_bangalore():
    pass

@olx_routes.route("/olx/pune",methods=["GET"])
def olx_pune():
    pass