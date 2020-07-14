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
    phone = db.Column(db.String(100))
    state = db.Column(db.String(100))
    city = db.Column(db.String(100))
    symptoms = db.Column(db.String(255))

    def __init__(self, name, age, sex, phone, state, city,symptoms):
        self.name = name
        self.age = age
        self.sex = sex
        self.phone = phone
        self.state = state
        self.city = city
        self.symptoms = symptoms


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
        phone = request.form['phone']
        state = request.form['state']
        city = request.form['city']
        symp = request.form.getlist('symptom')
        symptoms = ','.join(symp)

        my_report = citizen_report(name,age,sex,phone,state,city,symptoms)
        db.session.add(my_report)
        db.session.commit()

        return redirect(url_for('report'))

@app.route('/patient')
def patient():
    return render_template('patient.html')

@app.route('/report',methods=['GET','POST'])
def report():

    if request.method == 'POST':

        result = citizen_report.query.filter_by(phone = request.form['phone']).first()
        return render_template('report.html',result=result)

    return render_template('report.html')