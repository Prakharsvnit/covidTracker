from flask import (
    Flask,
    redirect,
    render_template,
    request,
    url_for
)

app = Flask(__name__)
app.secret_key = 'somesecretkeythatonlyishouldknow'
    

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':


        username = request.form['username']
        password = request.form['password']
        
        if username == "Peter" and password == "parker":
            return redirect(url_for('patient'))

    return render_template('index.html')

@app.route('/patient')
def patient():
    return render_template('patient.html')