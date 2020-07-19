from run import db

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
