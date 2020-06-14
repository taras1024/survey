import cs50
import csv

from flask import Flask, abort, jsonify, redirect, render_template, request
from werkzeug.exceptions import default_exceptions, HTTPException

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


@app.route("/form", methods=["POST"])
def post_form():

    name = request.form.get("name")
    house = request.form.get("house")
    position = request.form.get("position")

    if not name:
        abort(400,"missing Name")
    if not house:
        abort(400, "missing House")
    if not position:
        abort(400, "missing position")


    with open("survey.csv", "a", newline = "") as csvfile:
        writer = csv.writer(csvfile, quotechar = "|", quoting = csv.QUOTE_MINIMAL)
        writer.writerow([name, house, position])


    #return render_template("sheet.html")
    return redirect("/sheet")

@app.route("/sheet", methods=["GET"])
def get_sheet():

    with open('survey.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, quotechar='|')
        data = list(reader)

    return render_template("sheet.html", data = data)


@app.errorhandler(HTTPException)
def errorhandler(error):
    """Handle errors"""
    return render_template("error.html", error=error), error.code