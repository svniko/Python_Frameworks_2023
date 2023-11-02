from flask import Flask, render_template, request, url_for, redirect, flash, session
import random
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,  BooleanField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests

# daterime.datetime.utcnow

app = Flask(__name__, template_folder='templates')
# app.secret_key = '1231231secretkey or very'
app.config['SECRET_KEY'] = "f669374220c12ea4819ff8c971684ca1"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 	False

db = SQLAlchemy(app)

class FirstForm(FlaskForm):
    name = StringField("Enter you name", 
                       validators = [DataRequired()])
    submit = SubmitField("Submit")

class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable=False) 
    email = db.Column(db.String(120), nullable=False, unique = True)
    date_added = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return f"<Name>: {self.name}"

class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email=StringField("Email", validators=[DataRequired()])
    submit=SubmitField('Submit')


class SecondForm(FlaskForm):
    width = StringField("Enter a width", validators=[DataRequired()])
    height = StringField('Enter a height', 
				validators=[DataRequired()])
    is_black = BooleanField("Grayscale?")
    submit = SubmitField('Submit')

@app.route('/exchange_to/')
def exchange_to():
    # from_ ='USD'
    # to= 'UAH'
    # q = '_'.join((from_,to))
    q = request.args.get('q')
    from_, to = q.split('_')
    #double parentheses because the argument of join should be iterable (tuple in this case)
    p = {'apiKey':'3936b045e5345a0340b1', 'q':q}
    url = 'https://free.currconv.com/api/v7/convert'
    response = requests.get(url,params=p)
    if response and response.json()['results']:
        resp = response.json()
        convert = round(resp['results'][q]['val'],2)
        return f'<h1>1 {from_} is {convert} {to} </h1>'
    else:
        return f"<h1>Can't find the information to convert {from_} to {to} </h1>"



@app.route('/city/')
def search_city():
    API_KEY = 'c124fdaaa610d8f8091ce555740c7cd8'
    # initialize your key here
    city = request.args.get('q')  # city name passed as argument
   
    # call API and convert response into Python dictionary
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
    response = requests.get(url).json()

    if response.get('cod') == 200: 
        curr_temp = response['main']['temp']
        curr_temp_cels = round(curr_temp-273.15,2)
        return f'<h1> Current temperature in {city.title()} is {curr_temp_cels} &#8451;'
	        
    else:
        return f'<h1>Error getting temperature for {city.title()}</h1>'



@app.route('/lect6/', methods=['GET','POST'])
def lect6():
    w = h = None
    url = 'https://placekitten.com'
    form = SecondForm()
    if form.validate_on_submit():
        w = form.width.data
        h = form.height.data
        i = form.is_black.data
        form.width.data = ''
        form.height.data = ''
        form.is_black.data = False
  
        if (requests.get(url).status_code == 200):
            if i:
                url = url+"/g/"+str(w)+'/'+str(h)
            else:
                url = url+"/"+str(w)+'/'+str(h)
    return render_template('lecture6.html', form=form, url=url, w=w, h=h)


@app.route('/user/add/', methods=["GET","POST"])
def add_user():
    form=UserForm()
    our_users = []
    if form.validate_on_submit():
        
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
            flash(f"User {form.name.data} added successfully")
        form.name.data = ''
        form.email.data = ''
        
        our_users = Users.query.order_by(Users.date_added)
    return render_template("lecture5.jinja",
                            form=form,
                            our_users=our_users)

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


@app.route('/lect4/', methods=['GET', 'POST'])
def lect4():
    # name = None
    
    form = FirstForm()
    if form.validate_on_submit():
        # name = form.name.data
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('lect4'))
    return render_template('lecture4.jinja',
                            title = 'Lecture 4',
                            name = session.get('name'),
                            # name = name,
                            form = form)

# if __name__ == "__main__":
#     app.run(debug=True)

from flask import jsonify
import json

@app.route('/users_json', methods=['GET'])
def get_users():
    users = Users.query.all()
    
    # Convert to a list of dictionaries
    user_list = [{'id': user.id, 
                  'username': user.name, 
                  'email': user.email} 
                  for user in users]

     
    with open('data.json', 'w') as json_file:
        json.dump(user_list, json_file)
    
    return jsonify(users=user_list)
