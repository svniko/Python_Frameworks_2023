from flask import Flask, render_template

app = Flask(__name__, template_folder='templates')

@app.route("/")
def hello_world():
    return "<h1>Hello, Flask!</h1>"

@app.route("/about")
def about():
    return "<h1>About page</h1>"

# Ctrl+/

@app.route("/user/<name>")
def user(name):
    return f"<h1>Hello, {name}</h1>"

# @app.route("/<name>")
# def home(name):
#     return render_template('home.html', 
#                             name=name, 
#                             age=20)

@app.route("/users")
def home():
    name, age, profession = 'Jerry', 24, 'Programmer'
    template_context = dict(name=name, age=age, profession=profession)
    return render_template('home.html', 
                           **template_context)


# if __name__ == "__main__":
#     app.run(debug=True)