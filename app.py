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


class patient_detail(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    age = db.Column(db.String(100))
    sex = db.Column(db.String(100))
    state = db.Column(db.String(100))
    city = db.Column(db.String(100))
    status = db.Column(db.String(100))

    def __init__(self, name, age, sex, state, city, status):
        self.name = name
        self.age = age
        self.sex = sex
        self.state = state
        self.city = city
        self.status = status       

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':


        username = request.form['username']
        password = request.form['password']
        
        if username == "Peter" and password == "parker":
            return redirect(url_for('patient'))

    return render_template('index.html')

@app.route('/insertReport',methods=['POST'])
def insertReport():
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

@app.route('/insertPatient',methods=['POST'])
def insertPatient():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        sex = request.form.get('sex')
        state = request.form['state']
        city = request.form['city']
        status = request.form.get('status')

        my_detail = patient_detail(name,age,sex,state,city,status)
        db.session.add(my_detail)
        db.session.commit()

        return redirect(url_for('statistics'))

@app.route('/statistics')
def statistics():

    stats = patient_detail.query.all()
    return render_template('statistics.html',stats=stats)

@app.route('/patient')
def patient():
    return render_template('patient.html')

@app.route('/report',methods=['GET','POST'])
def report():

    if request.method == 'POST':

        result = citizen_report.query.filter_by(phone = request.form['phone']).all()
        return render_template('report.html',result=result)


    return render_template('report.html')
