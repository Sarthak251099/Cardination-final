from flask import render_template, url_for, flash, redirect, request , Blueprint
from cardination.doctor.forms import RegisterDoc, AddRecordDoc
from cardination.patient.forms import LoginForm 
from cardination.models import Patient, Doctor, User, Record
from cardination import db, bcrypt
from flask_login import login_user, current_user, login_required,logout_user
from cardination.main.utils import login_required

doctor = Blueprint('doctor',__name__)

@doctor.route("/registerDoc", methods=['GET', 'POST'])
def registerDoc():
    form = RegisterDoc()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(urole='Doctor')
        db.session.add(user)
        db.session.commit()
        doctor = Doctor(id = user.id, username = form.username.data,email = form.email.data,password=hashed_password,specialization=form.specialization.data,degree=form.degree.data,phone_number=form.phonenumber.data,address=form.address.data)
        db.session.add(doctor)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('doctor.loginDoc'))
    return render_template('registerDoc.html', title='Register Doctor', form=form)

@doctor.route("/loginDoc", methods=['GET', 'POST'])
def loginDoc():
    form = LoginForm()
    if form.validate_on_submit():
        doctor = Doctor.query.filter_by(email = form.email.data).first()
        if doctor and bcrypt.check_password_hash(doctor.password,form.password.data):
            user = doctor.user
            login_user(user,remember = form.remember.data)
            return redirect(url_for('doctor.viewRecordsDoc'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('loginDoc.html', title='Login Doctor', form=form)

@doctor.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))

@doctor.route("/accountDoc")
@login_required(role='Doctor')
def accountDoc():
    doc = Doctor.query.filter_by(id=current_user.id).first()
    if doc:
        image_file=url_for('static',filename='profile_pic/'+Doctor.query.filter_by(id=current_user.id).first().image_file)
        return render_template('accountDoc.html',image_file=image_file, doc=doc)
    else:
        return redirect(url_for('doctor.logout'))

@doctor.route("/addRecordDoc",methods=["POST","GET"])
@login_required(role="Doctor")
def addRecordDoc():
    form = AddRecordDoc()
    if form.validate_on_submit():
        pat = Patient.query.filter_by(username=form.patient.data).first()
        doctorRecord = Record(date=form.date.data, symptoms = form.symptoms.data,disease=form.disease.data,prescription=form.prescription.data,patient_id=pat.id,doctor_id=current_user.id)
        db.session.add(doctorRecord)
        db.session.commit()
        flash(f'Record added Successfully', 'success')
        return redirect(url_for('doctor.viewRecordsDoc'))
    return render_template('addRecordDoc.html', title='Add Record', form=form)

@doctor.route("/viewRecordsDoc")
@login_required(role="Doctor")
def viewRecordsDoc():
    record = Record.query.filter_by(doctor_id=current_user.id).all()
    return render_template('viewRecordsDoc.html',records = record)
