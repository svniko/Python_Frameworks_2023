from flask import Flask, render_template, request

app = Flask(__name__, template_folder='templates')

pets = [
    {'kind':'cat',
    'name':'Tom',
    'age':10,
    'color': 'grey'
    },
    {'kind':'cat',
    'name':'Barsik',
    'age':5,
    'color': 'white'
    },
    {'kind':'dog',
    'name':'Spike',
    'age':2,
    'color': 'brown'
    },
]

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
    return render_template('home.html.jinja', 
                           **template_context)

@app.route('/pet')
def pet():
    return render_template('pets.html.jinja', 
                            pets=pets,
                            title='Our pets')

@app.route('/lect2')
def lect2():
    return render_template('lecture2.jinja')

@app.route('/hello', methods=['GET', 'POST'])
def smb():
    if request.method == "GET":
        return render_template('hello.jinja', name='stranger')
    else:
        name = request.form.get('name')
        if not name:
            return render_template('lecture2.jinja', flag=0)
        return render_template('hello.jinja', name=name)

@app.errorhandler(405)
def method_not_allowed(e):
    return render_template('405.jinja', title='405 error'), 405


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.jinja', title='404 error'), 404
    
# if __name__ == "__main__":
#     app.run(debug=True)