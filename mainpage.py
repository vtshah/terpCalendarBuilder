import os
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/add_class/", methods = ['POST'])
def add_class():
    title = request.form["title"]
    section = request.form["section"]
    os.system("solution.py " + title.upper() +" "+section.upper())
    return render_template('completed.html')

if __name__ == "__main__":
    app.run(debug=True)
