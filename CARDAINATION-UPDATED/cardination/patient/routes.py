from flask import render_template, url_for, flash, redirect, request, Blueprint
from cardination.patient.forms import RegistrationForm, LoginForm, AddRecordPat, Diagnose
from cardination.models import Patient, Doctor, User, Record
from cardination import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from cardination.main.utils import login_required, predict

patient = Blueprint('patient',__name__)

@patient.route("/registerPatient", methods=['GET', 'POST'])
def registerPatient():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(urole='Patient')
        db.session.add(user)
        db.session.commit()
        patient = Patient(id = user.id, username = form.username.data,email = form.email.data,password=hashed_password,weight=form.weight.data,height=form.height.data,gender=form.gender.data,bloodgroup=form.bloodgroup.data,dob=request.form.get('DOB'))
        db.session.add(patient)
        db.session.commit()
        flash(f'Account created for {form.username.data}, Now you can login!', 'success')
        return redirect(url_for('patient.loginPatient'))
    return render_template('registerPatient.html', title='Register Patient', form=form)

@patient.route("/loginPatient", methods=['GET', 'POST'])
def loginPatient():
    if current_user.is_authenticated:
        return redirect(url_for('patient.accountPat'))
    form = LoginForm()
    if form.validate_on_submit():
        patient = Patient.query.filter_by(email = form.email.data).first()
        if patient and bcrypt.check_password_hash(patient.password,form.password.data):
            user = patient.user
            login_user(user,remember = form.remember.data)
            next_page = request.args.get('next')
            return redirect(url_for('next_page')) if next_page else redirect(url_for('patient.viewRecordsPat'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('loginPatient.html', title='Login Patient', form=form)

@patient.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))

@patient.route("/accountPat")
@login_required(role = 'Patient')
def accountPat():
    pat = Patient.query.filter_by(id=current_user.id).first()
    if pat:
        image_file=url_for('static',filename='profile_pic/'+ Patient.query.filter_by(id=current_user.id).first().image_file)
        return render_template('accountPat.html',image_file=image_file, pat=pat)


@patient.route("/addRecordPat",methods=["POST","GET"])
@login_required(role = "Patient")
def addRecordPat():
    form = AddRecordPat()
    if form.validate_on_submit():
        doc = Doctor.query.filter_by(username=form.doctor.data).first()
        patientRecord = Record(date=form.date.data, symptoms = form.symptoms.data,disease=form.disease.data,prescription=form.prescription.data,patient_id=current_user.id,doctor_id=doc.id)
        db.session.add(patientRecord)
        db.session.commit()
        flash(f'Record added Successfully', 'success')
        return redirect(url_for('patient.viewRecordsPat'))
    return render_template('addRecordPat.html', title='Add Record', form=form)

@patient.route("/viewRecordsPat")
@login_required(role="Patient")
def viewRecordsPat():
    record = Record.query.filter_by(patient_id=current_user.id).all()
    return render_template('viewRecordsPat.html',records = record)


@patient.route("/diagnose",methods=["POST","GET"])
@login_required(role="Patient")
def diagnose():
    form = Diagnose()
    if form.validate_on_submit():
        symptom = form.symptom.data
        symptoms = symptom.split(",")
        simp = []
        all_symptom = ['itching','skin_rash','nodal_skin_eruptions','sneezing','shivering','chills','joint_pain','stomach_pain','acidity','ulcers_on_tongue','muscle_wasting','vomiting','burning_micturition','spotting_ urination','fatigue','weight_gain','anxiety','cold_hands_and_feets','mood_swings','weight_loss','restlessness','lethargy','patches_in_throat','irregular_sugar_level','cough','fever','sunken_eyes','breathlessness','sweating','dehydration','indigestion','headache','yellowish_skin','dark_urine','nausea','loss_of_appetite','pain_behind_the_eyes','back_pain','constipation','abdominal_pain','diarrhoea','mild_fever','yellow_urine','yellowing_of_eyes','acute_liver_failure','fluid_overload','swelling_of_stomach','swelled_lymph_nodes','malaise','blurred_and_distorted_vision','phlegm','throat_irritation','redness_of_eyes','sinus_pressure','runny_nose','congestion','chest_pain','weakness_in_limbs','fast_heart_rate','pain_during_bowel_movements','pain_in_anal_region','bloody_stool','irritation_in_anus','neck_pain','dizziness','cramps','bruising','obesity','swollen_legs','swollen_blood_vessels','puffy_face_and_eyes','enlarged_thyroid','brittle_nails','swollen_extremeties','excessive_hunger','extra_marital_contacts','drying_and_tingling_lips','slurred_speech','knee_pain','hip_joint_pain','muscle_weakness','stiff_neck','swelling_joints','movement_stiffness','spinning_movements','loss_of_balance','unsteadiness','weakness_of_one_body_side','loss_of_smell','bladder_discomfort','foul_smell_of urine','continuous_feel_of_urine','passage_of_gases','internal_itching','toxic_look_(typhos)','depression','irritability','muscle_pain','altered_sensorium','red_spots_over_body','belly_pain','abnormal_menstruation','dischromic _patches','watering_from_eyes','increased_appetite','polyuria','family_history','mucoid_sputum','rusty_sputum','lack_of_concentration','visual_disturbances','receiving_blood_transfusion','receiving_unsterile_injections','coma','stomach_bleeding','distention_of_abdomen','history_of_alcohol_consumption','fluid_overload','blood_in_sputum','prominent_veins_on_calf','palpitations','painful_walking','pus_filled_pimples','blackheads','scurring','skin_peeling','silver_like_dusting','small_dents_in_nails','inflammatory_nails','blister','red_sore_around_nose','yellow_crust_ooze']
        for i in range(len(symptoms)):
            symptoms[i] = (symptoms[i].strip()).replace(" ", "_")
            if symptoms[i] in all_symptom:
                simp.append(symptoms[i])
        disease = predict(simp)
        flash(f'Disease Diagnosed is {disease}', 'success')
    return render_template('diagnose.html', title='Diagnosis', form=form)
