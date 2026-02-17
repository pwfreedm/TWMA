from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)


@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/form")
def form():
    return render_template("home_info.html")

@app.route("/submit", methods=["POST"])
def submit():

    #todo: figure out how to send off request.form to the controller
    return redirect(url_for('landing'))

if __name__ == "__main__":
    app.run(debug=True)
