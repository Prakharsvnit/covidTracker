from flask import (
    Flask,
    redirect,
    render_template,
    request,
    url_for,
    make_response
)
from fpdf import FPDF
from flask_sqlalchemy import SQLAlchemy
import pygal

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

    up_active = len( patient_detail.query.filter_by(state="Uttar Pradesh",status="Active").all())
    up_recovered = len( patient_detail.query.filter_by(state="Uttar Pradesh",status="Recovered").all())
    up_deceased = len( patient_detail.query.filter_by(state="Uttar Pradesh",status="Deceased").all())
    mp_active = len( patient_detail.query.filter_by(state="Madhya Pradesh",status="Active").all())
    mp_recovered = len( patient_detail.query.filter_by(state="Madhya Pradesh",status="Recovered").all())
    mp_deceased = len( patient_detail.query.filter_by(state="Madhya Pradesh",status="Deceased").all())
    maha_active = len( patient_detail.query.filter_by(state="Maharashtra",status="Active").all())
    maha_recovered = len( patient_detail.query.filter_by(state="Maharashtra",status="Recovered").all())
    maha_deceased = len( patient_detail.query.filter_by(state="Maharashtra",status="Deceased").all())
    guj_active = len( patient_detail.query.filter_by(state="Gujarat",status="Active").all())
    guj_recovered = len( patient_detail.query.filter_by(state="Gujarat",status="Recovered").all())
    guj_deceased = len( patient_detail.query.filter_by(state="Gujarat",status="Deceased").all())
    del_active = len( patient_detail.query.filter_by(state="Delhi",status="Active").all())
    del_recovered = len( patient_detail.query.filter_by(state="Delhi",status="Recovered").all())
    del_deceased = len( patient_detail.query.filter_by(state="Delhi",status="Deceased").all())

    line_chart = pygal.Bar()
    line_chart.title = 'Covid-19 cases in different states'
    line_chart.x_labels = ['Uttar Pradesh','Madhya Pradesh','Maharashtra','Gujarat','Delhi']
    line_chart.add('Active',[up_active,mp_active,maha_active,guj_active,del_active] )
    line_chart.add('Recovered',[up_recovered,mp_recovered,maha_recovered,guj_recovered,del_recovered])
    line_chart.add('Deceased',[up_deceased,mp_deceased,maha_deceased,guj_deceased,del_deceased])
    chart_data = line_chart.render_data_uri()


    stats = patient_detail.query.all()
    return render_template('statistics.html',stats=stats,chart_data=chart_data)

@app.route('/patient')
def patient():
    return render_template('patient.html')

@app.route('/report',methods=['GET','POST'])
def report():

    if request.method == 'POST':

        result = citizen_report.query.filter_by(phone = request.form['phone']).all()
        for row in result:

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial","BU",size=30)
            pdf.cell(190,30,txt ="Your Covid-19 report",ln=1, align="C")
            pdf.set_font("")
            pdf.set_font("Arial",size=20)
            pdf.cell(90,20,txt ="Name :",ln=0,align="R")
            pdf.cell(100,20,txt = row.name,ln=1,align="L")
            pdf.cell(90,20,txt ="Age :",ln=0,align="R")
            pdf.cell(100,20,txt = row.age,ln=1,align="L")
            pdf.cell(90,20,txt ="Sex :",ln=0,align="R")
            pdf.cell(100,20,txt = row.sex,ln=1,align="L")
            pdf.cell(90,20,txt ="Phone :",ln=0,align="R")
            pdf.cell(100,20,txt = row.phone,ln=1,align="L")
            pdf.cell(90,20,txt ="State :",ln=0,align="R")
            pdf.cell(100,20,txt = row.state,ln=1,align="L")
            pdf.cell(90,20,txt ="City :",ln=0,align="R")
            pdf.cell(100,20,txt = row.city,ln=1,align="L")
            pdf.set_font("Arial",size=10)
            pdf.cell(50,20,txt ="Symptoms :",ln=0,align="L")
            pdf.cell(100,20,txt = row.symptoms,ln=1,align="L")
            pdf.set_font("Arial",size=15)
            list = row.symptoms.split(',')
            if len(list) >= 4:
                a = "You need to get tested for Covid-19 at nearest hospital"
                pdf.cell(150,20,txt=a,ln=1,align="C")
            else:
                b = "You need to take precautions"
                pdf.cell(100,20,txt=b,ln=1,align="C")
            pdf.set_font("Arial",size=20)

            response = make_response(pdf.output(dest='S').encode('latin-1'))
            response.headers.set('Content-Disposition', 'attachment', filename='report' + '.pdf')
            response.headers.set('Content-Type', 'application/pdf')
            return response
        return render_template('report.html',result=result)

    return render_template('report.html')



if __name__ == "__main__":
    app.run()