from flask import Flask,render_template,url_for,redirect,jsonify,flash,request,send_file,session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin,login_user,LoginManager,login_required,logout_user,current_user
from flask_bcrypt import Bcrypt
from datetime import datetime,date
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,TextAreaField,SelectField
from wtforms.validators import InputRequired,Length, ValidationError,Email,DataRequired,EqualTo
from flask_migrate import Migrate
from flask_cors import CORS
import os
import xlsxwriter
import pandas as pd
from flask_mail import Mail,Message
from werkzeug.security import generate_password_hash, check_password_hash

app=Flask(__name__)
bcrypt=Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///test.db"
app.config["SECRET_KEY"]='thisisasecretkey'

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///test.db"
app.config["SECRET_KEY"]='thisisasecretkey'
db=SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


migrate=Migrate(app,db,render_as_batch=True)
cors=CORS(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']='healios.ai31@gmail.com'
app.config['MAIL_PASSWORD']='mtkwamvitfkanudb'
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True

mail=Mail(app)

class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50),nullable=False,unique=True)
    password=db.Column(db.String(50),nullable=False)
   

class Bond(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(80))
    content=db.Column(db.Text,nullable=False)
    author=db.Column(db.String(80),nullable=False)
    date_posted=db.Column(db.DateTime,default=datetime.now)
    tags=db.Column(db.String(200),nullable=False)
    

class Comments(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    commentID=db.Column(db.Integer)
    content=db.Column(db.Text,nullable=False)
    author=db.Column(db.String(80),nullable=False)
    date_posted=db.Column(db.DateTime,default=datetime.now)

class Like(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    likeID=db.Column(db.Integer)
    author=db.Column(db.String(80),nullable=False)
    date_posted=db.Column(db.DateTime,default=datetime.now)

class Docs(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(50),nullable=False,unique=True)
    name=db.Column(db.String(50),nullable=False)
    qualifications=db.Column(db.String(50),nullable=False)
    specialties=db.Column(db.String(50),nullable=False)
    password=db.Column(db.String(50),nullable=False)
    description=db.Column(db.Text,nullable=True)
    
class Appointments(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    email=db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    time = db.Column(db.String(5), nullable=False)
    status = db.Column(db.String(20), default="Pending") 
    author=db.Column(db.String(50),nullable=False)
    doctor=db.Column(db.String(50),nullable=False)

class Prescriptions(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    patient_name=db.Column(db.String(100),nullable=False)
    doctor_name=db.Column(db.String(100),nullable=False)
    email=db.Column(db.String(100),nullable=False)
    medication=db.Column(db.String(100),nullable=False)
    dosage=db.Column(db.String(100),nullable=False)
    instructions=db.Column(db.String(100),nullable=False)
    diagnosis=db.Column(db.String(100),nullable=False)

class RegisterForm(FlaskForm):
    username=StringField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={"placeholder":"Username"})
    password=PasswordField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={"placeholder":"Password"})
    submit=SubmitField("Submit")
    def validate_username(form,username):
        existing_user=User.query.filter_by(username=username.data).first()

        if existing_user:
            flash("This usernamealready exists",'info')
            raise ValidationError("This username already exists")
    

class Login(FlaskForm):
    username=StringField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={'placeholder':'username'})
    password=PasswordField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={'placeholder':'Password'})

    submit=SubmitField('Submit')

class Bond_page(FlaskForm):
    title=StringField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={'placeholder':'Enter Title'})
    content=TextAreaField("Your views matter a lot",render_kw={'placeholder':'Share your views'})
    submit=SubmitField("Post your views")
    tags=StringField(validators=[InputRequired(),Length(min=4,max=200)],render_kw={'placeholder':'Tags'})

class CommentForm(FlaskForm):
    comment=TextAreaField(render_kw={'placeholder':'Comment here'})
    submit=SubmitField('Post')

class LikeForm(FlaskForm):
    submit=SubmitField('Like')

class DoctorDetails(FlaskForm):
    email=StringField(validators=[InputRequired(),Length(min=4,max=50)],render_kw={"placeholder":"Email"})
    name=StringField(validators=[InputRequired(),Length(min=4,max=100)],render_kw={"placeholder":"Name"})
    qualifications=StringField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={"placeholder":"Degrees"})
    specialties=StringField(validators=[InputRequired(),Length(min=4,max=100)],render_kw={"placeholder":"Specialties"})
    password=PasswordField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={"placeholder":"Password"})
    
    submit=SubmitField("Submit")
    def validate_username(form,email):
        existing_doctor=Docs.query.filter_by(email=email.data).first()

        if existing_doctor:
            flash("This usernamealready exists",'info')
            raise ValidationError("This username already exists")
     
class doctor_login(FlaskForm):
    email=StringField(validators=[InputRequired(),Length(min=4,max=50)],render_kw={"placeholder":"Email"})
    password=PasswordField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={"placeholder":"Password"})
    submit=SubmitField("Submit")

class DescriptionForm(FlaskForm):
    description = TextAreaField('Description', render_kw={'placeholder': 'Write your description here...'})
    submit = SubmitField('Submit')

class FeedbackForm(FlaskForm):
    name=StringField('Name',validators=[InputRequired(),Length(min=2,max=50)])
    email=StringField('Email',validators=[InputRequired(),Email()])
    message=TextAreaField('Message',validators=[InputRequired(), Length(min=10, max=500)])
    submit=SubmitField('Submit')

class AppointmentForm(FlaskForm):
    name=StringField('Name',validators=[InputRequired()])
    email=StringField('Email',validators=[InputRequired(),Email()])
    date=StringField('Date',validators=[InputRequired()])
    time=StringField('time',validators=[InputRequired()])
    doctor=StringField('doctor',validators=[InputRequired()])
    submit=SubmitField('Submit')

class StatusForm(FlaskForm):
    status=SelectField('Status',choices=[('Accepted', 'Accept'), ('Rejected', 'Reject')])
    submit=SubmitField('Submit')

class PresciptionForm(FlaskForm):
    name=StringField('Patient Name',validators=[InputRequired()])
    email=StringField('Patient Email',validators=[InputRequired(),Email()])
    doctor_name=StringField('Doctors Name',validators=[InputRequired()])
    medication=StringField('Medication',validators=[InputRequired()])
    dosage = StringField('Dosage', validators=[InputRequired()])
    instructions = TextAreaField('Instructions', validators=[InputRequired()])
    diagnosis=StringField('Diagnosis', validators=[InputRequired()])
    submit=SubmitField('Submit')

e_prescription=[]



class Users(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(80),nullable=False)
    email=db.Column(db.String(80),nullable=False)
    username=db.Column(db.String(80),unique=True,nullable=False)
    password=db.Column(db.String(80),nullable=False)
    role=db.Column(db.String(80),nullable=False)


class DoctorVerification(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'), nullable=False)
    qualification = db.Column(db.String(200), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    license_number = db.Column(db.String(100), unique=True, nullable=False)
    years_of_experience = db.Column(db.Integer, nullable=False)
    additional_info = db.Column(db.Text, nullable=True)
    is_verified = db.Column(db.Boolean, default=False)

    user = db.relationship('Users', backref=db.backref('doctor_verification', uselist=False))

class stepTracker(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'), nullable=False)
    steps=db.Column(db.Integer,nullable=False,default=0)
    date = db.Column(db.Date, default=date.today, nullable=False)

    user = db.relationship('Users', backref=db.backref('steps', lazy=True))

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    name=StringField('Name', validators=[DataRequired()])
    email=StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('patient', 'Patient'), ('doctor', 'Doctor'), ('admin', 'Admin')])
    submit = SubmitField('Register')

    

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class DoctorVerificationForm(FlaskForm):
    qualification = StringField('Qualification', validators=[DataRequired()])
    specialization = StringField('Specialization', validators=[DataRequired()])
    license_number = StringField('License Number', validators=[DataRequired()])
    years_of_experience = StringField('Years of Experience', validators=[DataRequired()])
    additional_info = TextAreaField('Additional Information (Optional)')
    submit = SubmitField('Submit')


@app.route('/')
def index():
    if current_user.is_authenticated:
         print(current_user.username)
         return render_template('user_dashboard.html', user=current_user.username)
    else:
         return render_template('user_dashboard.html', user=None)  
    

@app.route('/register',methods=['GET','POST'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        hash_password=generate_password_hash(form.password.data)
        new_user=Users(name=form.name.data,email=form.email.data,username=form.username.data,password=hash_password,role=form.role.data)
        db.session.add(new_user)
        db.session.commit()


        if form.role.data=='doctor':
            return redirect(url_for('doctor_verification',user_id=new_user.id))
        
        return redirect(url_for('login'))
    return render_template('register.html',form=form)
        
@app.route('/doctor_verification/<int:user_id>',methods=['GET','POST'])
def doctor_verification(user_id):
    doctor_to_verify=Users.query.get_or_404(user_id)
    form=DoctorVerificationForm()
    if form.validate_on_submit():
        verification_data=DoctorVerification(user_id=user_id,qualification=form.qualification.data,
            specialization=form.specialization.data,
            license_number=form.license_number.data,
            years_of_experience=form.years_of_experience.data,
            additional_info=form.additional_info.data)
        db.session.add(verification_data)
        db.session.commit()
        return redirect(url_for('verification_pending'))
    return render_template('doctor_verification.html',form=form)


@app.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user_in=Users.query.filter_by(username=form.username.data).first()
        if user_in and check_password_hash(user_in.password,form.password.data):
            login_user(user_in)

            if user_in.role=='doctor':
                doctor_in=DoctorVerification.query.filter_by(user_id=user_in.id).first()
                if not doctor_in.is_verified:
                    return redirect(url_for('verification_pending'))
            return redirect(f'{user_in.role}_dashboard')
    return render_template('login.html',form=form)
    
@app.route('/doc_login',methods=['GET','POST'])
def doc_login():
    form=LoginForm()
    if form.validate_on_submit():
        doctor_in=Users.query.filter_by(username=form.username.data).first()
        if doctor_in and check_password_hash(doctor_in.password,form.password.data) and doctor_in.role=='doctor':
            doctor_verify=DoctorVerification.query.filter_by(user_id=doctor_in.id).first()
            if not doctor_verify.is_verified:
                return redirect(url_for('verification_pending'))
            login_user(doctor_in)
            return redirect(url_for('doctor_dashboard'))
    return render_template('doctor_login.html',form=form)



@app.route('/patient_dashboard',methods=['GET','POST'])
@login_required
def user_dashboard():
    user=current_user
    return render_template('user_dashboard.html',user=user)

@app.route('/doctor_dashboard',methods=['GET','POST'])
@login_required
def doctor_dashboard():
    if current_user.role!='doctor':
        return redirect(url_for('index'))
    doctor_logged=current_user
    return render_template('doctor_dashboard.html',doctor_logged=doctor_logged)


@app.route('/admin_dashboard', methods=['GET', 'POST'])
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('index'))
    doctors_to_verify = DoctorVerification.query.filter_by(is_verified=False).all()
    
    if request.method == 'POST':
        doctor_id = int(request.form.get('doctor_id'))
        action = request.form.get('action')
        doctor_verification = DoctorVerification.query.get_or_404(doctor_id)
        
        if action == 'verify':
            doctor_verification.is_verified = True
        elif action == 'reject':
            db.session.delete(doctor_verification)
        
        db.session.commit()
        flash(f'Doctor {action}ed successfully.', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('verify_doctors.html', doctors_to_verify=doctors_to_verify)

@app.route('/verification_pending',methods=['GET','POST'])
@login_required
def verification_pending():
    if current_user.role!='doctor':
        return redirect(url_for('index'))
    return render_template('verification_pending.html') 



@app.route('/bond',methods=['POST','GET'])
@login_required
def bonding():
    
    posts=Bond.query.order_by(Bond.date_posted.desc()).all()
    return render_template("bonding.html",posts=posts)

@app.route('/delete/<int:id>',methods=['GET','POST'])
@login_required
def delete_post(id):
    post=Bond.query.get_or_404(id)
    if post.author==current_user.name:
        try:
            db.session.delete(post)
            db.session.commit()
            return redirect(url_for('bonding'))
        except:
            return("You cant delete this post")
        
    else:
        return redirect('/patient_dashboard')
   
        
@app.route('/write',methods=['GET','POST'])
@login_required
def write():
    form=Bond_page()
    

    if form.validate_on_submit():
        post=Bond(content=form.content.data,author=current_user.name,title=form.title.data,tags=form.tags.data)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('bonding'))
    

    posts = Bond.query.filter_by(author=current_user.name).order_by(Bond.date_posted.desc()).all()
    
    return render_template('write.html',form=form,posts=posts)

@app.route('/comment/<int:id>',methods=['GET','POST'])
@login_required
def comment(id):
    post_comment=Bond.query.get_or_404(id)
    form=CommentForm()
    if form.validate_on_submit():
        user_comment=Comments(content=form.comment.data,author=current_user.username,commentID=post_comment.id)
        db.session.add(user_comment)
        db.session.commit()
        return redirect(url_for('bonding'))
    comments=Comments.query.filter_by(commentID=post_comment.id).order_by(Comments.date_posted.desc()).all()
    comments_count=Comments.query.filter_by(commentID=post_comment.id).count()
    return render_template('comment.html',post_comment=post_comment,comments=comments,form=form,comments_count=comments_count)

@app.route('/delete_comment/<int:id>')
@login_required
def delete_comment(id):
    comment_to_delete=Comments.query.get_or_404(id)
    if comment_to_delete.author==current_user.username:
        try:
            db.session.delete(comment_to_delete)
            db.session.commit()
            return redirect(url_for('bonding'))
        except:
            return("You cant delete this post")
        
    else:
        return redirect('/write')
    
@app.route('/like/<int:id>',methods=['GET','POST'])
@login_required
def like_post(id):
    liked_post=Bond.query.get_or_404(id)
    form=LikeForm()
    if form.validate_on_submit():
        # Check if the user already liked this post
        like = Like.query.filter_by(author=current_user.username, likeID=liked_post.id).first()
        if like:
            
            db.session.delete(like)
            db.session.commit()
            flash('You unliked this post.', 'success')
            return redirect(url_for('bonding'))
        else:
            
            new_like = Like(author=current_user.username, likeID=liked_post.id)
            db.session.add(new_like)
            db.session.commit()
            flash('You liked this post!', 'success')

        #try:
            #like=Like(likeID=liked_post.id,author=current_user.username)
            #db.session.add(like)
            #db.session.commit()
            #return redirect(url_for('bonding'))
        #except:
            return redirect(url_for('bonding'))
    like_count=Like.query.filter_by(likeID=liked_post.id).count()
    return render_template('like.html',form=form,like_count=like_count,liked_post=liked_post)

# @app.route('/doctor',methods=['GET','POST'])
# def doctor():
#     form=DoctorDetails()
#     if form.validate_on_submit():
#         hashed_doctor_pass=bcrypt.generate_password_hash(form.password.data)
#         new_doc=Docs(password=hashed_doctor_pass,name=form.name.data,email=form.email.data, qualifications=form.qualifications.data,specialties=form.specialties.data)
#         db.session.add(new_doc)
#         db.session.commit()
#         return redirect('/doc_login')
#     return render_template('doctor_signup.html',form=form)

# @app.route('/doc_login',methods=['GET','POST'])
# def doc_login():
#     form=doctor_login()
#     if form.validate_on_submit():
#         doctor_in=Docs.query.filter_by(email=form.email.data).first()
#         if doctor_in:
#             if bcrypt.check_password_hash(doctor_in.password,form.password.data):
#                 login_user(doctor_in)
#                 return redirect('/doc_page')

#     return render_template('doctor_login.html',form=form)

# @app.route('/doc_page',methods=['GET','POST'])
# @login_required
# def doctor_page():
#     doc_logged=current_user
#     return render_template('doc_page.html',doc_logged=doc_logged)

# @app.route('/doc_profile',methods=['GET','POST'])
# @login_required
# def doc_profile():
#     print(current_user.username)
#     doc_profile=current_user
#     return render_template('doc_profile.html',doc_profile=doc_profile)

@app.route('/doc_list',methods=['GET','POST'])
@login_required
def doc_list():
    res_doctors=DoctorVerification.query.all()
    return render_template('doc_list.html',res_doctors=res_doctors)

@app.route('/doc_details/<int:id>',methods=['GET','POST'])
@login_required
def consult(id):
    doc_to_book=DoctorVerification.query.get_or_404(id)
    return render_template('doc_details.html',doc_to_book=doc_to_book)

@app.route('/description/<int:id>',methods=['GET','POST'])
@login_required
def description(id):
    doc_des=Docs.query.get_or_404(id)
    form=DescriptionForm()
    if form.validate_on_submit():
        doc_des.description=form.description.data
        db.session.commit()
    return render_template('description.html',form=form,doc_des=doc_des)


@app.route('/video')
@login_required
def video():
    return render_template('video.html')

@app.route('/heartrate')
@login_required
def heartrate():
    return render_template('heartrate.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect ('/login')

def save_feedback_to_excel(name, email, message):
    file_path = 'feedback.xlsx'

    # Create a DataFrame for the new feedback
    new_feedback = pd.DataFrame([{'Name': name, 'Email': email, 'Message': message}])

    if os.path.exists(file_path):
        # Read existing data from the Excel file
        existing_data = pd.read_excel(file_path)

        # Concatenate existing data with the new feedback
        updated_data = pd.concat([existing_data, new_feedback], ignore_index=True)
    else:
        # If the file doesn't exist, use the new feedback as the initial data
        updated_data = new_feedback

    # Save the updated data back to the Excel file
    updated_data.to_excel(file_path, index=False)
    
@app.route('/feedback',methods=['GET','POST'])
@login_required
def feedback():
    form=FeedbackForm()
    if form.validate_on_submit():
        name=form.name.data
        email=form.email.data
        message=form.message.data
        save_feedback_to_excel(name,email,message)
        flash('Thank you for your feedback!', 'success')
        message=Message(subject='Your Feedback for Healios.ai',sender='healios.ai31@gmail.com',recipients=[email])
        message.body='Thanks for your feedback'
        mail.send(message)
        return redirect('/dashboard')
    return render_template('feedback.html',form=form)

@app.route('/download_feedback', methods=['GET'])
@login_required  # Ensures only logged-in users can access
def download_feedback():
   

    file_path = 'feedback.xlsx'
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        flash("The feedback file doesn't exist.", 'error')
        return redirect('/dashboard')

@app.route('/appointment',methods=['GET','POST'])
@login_required
def appointment():
    doctors=DoctorVerification.query.all()
    form=AppointmentForm()
    if form.validate_on_submit():
        print(current_user.name)
        appointment=Appointments(name=form.name.data,email=form.email.data,date=form.date.data,time=form.time.data,author=current_user.name,doctor=form.doctor.data) #current_user.username making error
        db.session.add(appointment)
        db.session.commit()
        return redirect('/patient_dashboard')
    return render_template('appointment.html',form=form,doctors=doctors)

@app.route('/schedule',methods=['GET','POST'])
@login_required
def schedule():
    print(current_user.name)
    appointment_scheduled=Appointments.query.filter_by(author=current_user.name).all()
    return render_template('schedule.html',appointment_scheduled=appointment_scheduled)

@app.route('/doctor_appointment',methods=['GET','POST'])
@login_required
def doctor_appointment():
    docs=DoctorVerification.query.all()
    appointments=Appointments.query.filter_by(status='Pending',doctor=current_user.name).all()
    form=StatusForm()
    if form.validate_on_submit():
        return redirect(url_for('doctor_appointments'))
    return render_template("doctor_appointments.html", appointments=appointments, form=form)

@app.route('/doctor_calender',methods=['GET','POST'])
@login_required
def doctor_calender():
    appointments=Appointments.query.filter_by(doctor=current_user.name).all()
    return render_template("doctor_calender.html",appointments=appointments)


@app.route('/update_status/<int:appointment_id>',methods=['GET','POST'])
def update_status(appointment_id):
    form=StatusForm()
    if form.validate_on_submit():
        appointment=Appointments.query.get_or_404(appointment_id)
        appointment.status=form.status.data
        db.session.commit()
        return redirect('/doctor_appointment')
    return render_template('doc_page')

@app.route('/prescription',methods=['GET','POST'])
@login_required
def prescription():
    docs=DoctorVerification.query.all()
    form=PresciptionForm()
    if form.validate_on_submit():
        prescrip=Prescriptions(patient_name=form.name.data,email=form.email.data,doctor_name=form.doctor_name.data,medication=form.medication.data,dosage=form.dosage.data,instructions=form.instructions.data,diagnosis=form.diagnosis.data)
        db.session.add(prescrip)
        db.session.commit()
        # prescription={
        #     'patient_name':form.name.data,
        #     'doctor_name':form.doctor_name.data,
        #     'medication':form.medication.data,
        #     'dosage':form.dosage.data,
        #     'instructions':form.instructions.data,
        #     'email':form.email.data
        # }
        # print("Adding prescription:", prescription)
        # e_prescription.append([prescription])
        email_patient=form.email.data
        if email_patient:
            try:
                msg=Message(subject='Your Prescription',sender='healios.ai31@gmail.com',recipients=[email_patient])
                msg.body = f"""\
Hello {form.name.data},

Your prescription details are as follows:
- Doctor: {form.doctor_name.data}
- Medication: {form.medication.data}
- Dosage: {form.dosage.data}
- Instructions: {form.instructions.data}
- Diagnosis: {form.diagnosis.data}

Take care,
Your Healthcare Provider
Healios.ai
"""
                # msg.body = (f"Patient Name: {prescription['patient_name']}\n"
                #             f"Doctor Name: {prescription['doctor_name']}\n"
                #             f"Medication: {prescription['medication']}\n"
                #             f"Dosage: {prescription['dosage']}\n"
                #             f"Instructions: {prescription['instructions']}")
                mail.send(msg)
                flash('Prescription emailed successfully!', 'success')
            except Exception as e:
                flash(f'Failed to send email: {e}', 'danger')
                return render_template('view.html')
    return render_template('prescription.html',form=form,docs=docs)

@app.route('/prescription/<int:id>')
def view_prescription(id):
    patient_prescription=Prescriptions.query.get_or_404(id)
    return render_template('view.html',patient_prescription=patient_prescription)
    
@app.route('/view')
@login_required
def view():
    session['doctor.user.name'] = current_user.name
    print(current_user.name)
    docs=DoctorVerification.query.all()
    user_in=current_user.name
    prescriptions=Prescriptions.query.filter_by(doctor_name=current_user.name).all()
    return render_template('prescription_list.html',prescriptions=prescriptions,user_in=user_in)

@app.route('/delete_prescription/<int:id>',methods=['GET','POST'])
@login_required
def delete_prescription(id):
    pres_to_delete=Prescriptions.query.get_or_404(id)
    try:
        db.session.delete(pres_to_delete)
        db.session.commit()
    except:
        return('You cant delete this post')
    return render_template('prescription_list.html')

@app.route('/steps',methods=['GET','POST'])
@login_required
def steps():
    steps=stepTracker.query.all()
    return render_template('steps.html',username=current_user.name,steps=steps)

@app.route('/update_steps',methods=['POST'])
@login_required
def update_steps():
    data=request.get_json()  #Pickup whole data from front end
    steps=data.get('steps',0) #pickup steps from data and if not found then put them equal to 0

    record=stepTracker.query.filter_by(user_id=current_user.id,date=date.today()).first()
    if record:
        record.steps=steps
    else:
        new_record=stepTracker(user_id=current_user.id,date=date.today(),steps=steps)
        db.session.add(new_record)
        db.session.commit()

@app.route('/get_steps',methods=['GET','POST'])
@login_required
def show_steps():
    step_history=stepTracker.query.filter_by(user_id=current_user.id).all()
    steps_list = [{"date": str(step.date), "steps": step.steps} for step in step_history]
    return jsonify(steps_list)

@app.route('/appointment_history',methods=['GET','POST'])
@login_required
def appointment_history():
    appointments=Appointments.query.filter_by(author=current_user.name).all()
    return render_template('appointment_history.html',appointments=appointments)


if __name__=='__main__':
    app.run(port=5000,debug=True, host='0.0.0.0')


