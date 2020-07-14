from flask import (
    Flask,
    redirect,
    render_template,
    request,
    url_for
)

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'somesecretkeythatonlyishouldknow'
    

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://prakhar:Password@123@localhost/covidtracker'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class citizen_report(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    age = db.Column(db.String(100))
    sex = db.Column(db.String(100))
    state = db.Column(db.String(100))
    city = db.Column(db.String(100))

    def __init__(self, name, age, sex, state, city):
        self.name = name
        self.age = age
        self.sex = sex
        self.state = state
        self.city = city


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':


        username = request.form['username']
        password = request.form['password']
        
        if username == "Peter" and password == "parker":
            return redirect(url_for('patient'))

    return render_template('index.html')

@app.route('/insert',methods=['POST'])
def insert():
    if request.method == 'POST':
        
        name = request.form['name']
        age = request.form['age']
        sex = request.form['sex']
        state = request.form['state']
        city = request.form['city']

        my_report = citizen_report(name,age,sex,state,city)
        db.session.add(my_report)
        db.session.commit()

        return redirect(url_for('login'))

@app.route('/patient')
def patient():
    return render_template('patient.html')