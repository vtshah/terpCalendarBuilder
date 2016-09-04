import os
from flask import Flask, render_template, request
from solution1y import mainFunction

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/add_class/", methods = ['POST'])
def add_class():
    title = request.form["title"]
    section = request.form["section"]
    mainFunction(title, section)
    #os.system('~/Downloads/terpCalendarBuilder/solution.py ' + title.upper() +' '+section.upper())
    return render_template('completed.html')

if __name__ == "__main__":
    app.run(debug=True)
