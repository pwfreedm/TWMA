from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)

# Landing page
@app.route("/")
def landing():
    return render_template("landing.html")

# Form page
@app.route("/form")
def form():
    return render_template("form.html")

# Handle form submission
@app.route("/submit", methods=["POST"])
def submit():

    #todo: figure out how to send off request.form to the controller
    return redirect(url_for('landing'))

if __name__ == "__main__":
    app.run(debug=True)
