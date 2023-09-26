from flask import Flask, render_template, request, url_for, redirect, flash
import random


app = Flask(__name__, template_folder='templates')
app.secret_key = '1231231secretkey or very'

game = {
    'choise': None,
    'you_win':0,
    'comp_win':0,
    'round': 0
    }



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

@app.route('/hello/', methods=['GET', 'POST'])
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


@app.route('/start/')
def start():
    return render_template('rsp.jinja',
                           title="Game", start=True )

@app.route('/select/<ch>/')
def select(ch):
    game['choise'] = ch
    return redirect(url_for('rsp'))

@ app.route('/game/')
def rsp():

    if game['round'] < 5:
        game['round'] += 1
        n = random.randint(0,2)
        # 0 -rock, 1-scissors, 2-paper
        if game['choise'] == '0' and n == 0:
            flash('Draw', category='warning')

        elif game['choise'] == '0' and n == 1:
            flash('You win', category='success')
            game['you_win'] +=1
        elif game['choise'] == '0' and n == 2:
            flash('Comp win', category='danger')
            game['comp_win'] +=1
        else: 
            pass

    else:
        if game['comp_win'] > game['you_win']:
            flash('Total Comp win', category='danger')
            redirect(url_for('rsp'))
        elif game['comp_win'] == game['you_win']:
            flash('Total Draw', category='warning')
            redirect(url_for('rsp'))
        else:
            flash('Total You Win. Congrats', category='success')
            redirect(url_for('rsp'))

    return render_template('rsp.jinja',
                           title="Game" )




# if __name__ == "__main__":
#     app.run(debug=True)