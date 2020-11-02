from datetime import datetime
from cardination import db,login_manager,app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    patient = db.relationship('Patient',backref = 'user',lazy = True)
    doctor = db.relationship('Doctor',backref = 'user',lazy = True)
    urole = db.Column(db.String(80),nullable=False)

    def __repr__(self):
        return f"User('{self.id}','{self.urole}')"

class Patient(db.Model):
    id = db.Column(db.Integer,db.ForeignKey('user.id'), primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    image_file = db.Column(db.String(20), nullable = False, default = 'default.jpg')
    password = db.Column(db.String(60), nullable = False)
    weight = db.Column(db.Integer, unique = False, nullable = True)
    height = db.Column(db.Integer, unique = False, nullable = True)
    gender = db.Column(db.String(1), unique = False, nullable = False)
    bloodgroup = db.Column(db.String(10), unique = False, nullable = True)
    dob = db.Column(db.String(20), unique = False, nullable = True)
    records = db.relationship('Record',backref='patient',lazy=True)

    def __repr__(self):
        return f"Patient('{self.username}', '{self.email}', '{self.image_file}', '{self.weight}', '{self.height}', '{self.gender}', '{self.bloodgroup}', '{self.dob}')"

class Doctor(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    image_file = db.Column(db.String(20), nullable = False, default = 'default.jpg')
    password = db.Column(db.String(60), nullable = False)
    specialization= db.Column(db.String(60), nullable = False)
    degree= db.Column(db.String(60), nullable = False)
    gender= db.Column(db.String(1), nullable = True)
    phone_number= db.Column(db.String(60), nullable = False)
    address= db.Column(db.String(120), nullable = True)
    records = db.relationship('Record',backref='doctor',lazy=True)

    def __repr__(self):
        return f"Doctor('{self.username}', '{self.email}', '{self.image_file}', '{self.specialization}', '{self.degree}', '{self.gender}', '{self.phone_number}', '{self.address}')"

class Record(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    date = db.Column(db.String(30),nullable=False,default=datetime.utcnow)
    symptoms = db.Column(db.String(20),nullable=True)
    disease = db.Column(db.String(20), nullable=False) 
    prescription = db.Column(db.String(20),nullable=False)
    additional_info = db.Column(db.Text)
    patient_id = db.Column(db.String(20),db.ForeignKey('patient.id'),nullable=False)
    doctor_id = db.Column(db.String(20),db.ForeignKey('doctor.id'),nullable=False)

    def __repr__(self):
        return f"Record('{self.id}', '{self.date}', '{self.symptoms}','{self.disease}','{self.prescription}','{self.additional_info}','{self.patient_id}', '{self.doctor_id}')"   