from flask import Flask, render_template, url_for, request,redirect, make_response, flash
from dbconnect import connection
import MySQLdb
import json
import numpy as np
from flask_login import LoginManager, login_user, current_user, logout_user, login_required, UserMixin
from flask_bcrypt import Bcrypt
import time    
from flask_mail import Mail, Message
import smtplib
from sendMessage import getClient
from setup import EMAIL_SERVER, EMAIL_ID, EMAIL_PASS, EMAIL_PORT, TWILIO_NUMBER


app = Flask(__name__)
app.config['SECRET_KEY'] = '24a92cbc4352146a46e0c61b51a13dca'
app.config['MAIL_SERVER'] = EMAIL_SERVER
app.config['MAIL_PORT'] = EMAIL_PORT
app.config['MAIL_USERNAME'] = EMAIL_ID
app.config['MAIL_PASSWORD'] = EMAIL_PASS
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


@app.route("/")
@app.route("/home", methods = ['GET','POST'])
def home():
    if(current_user.is_authenticated):
            return redirect('history')
    db, cursor = connection()
    cursor.execute('''SELECT * FROM host_entry''')
    data = cursor.fetchall()
    print(data)
    db.close()
    if(request.method == 'POST'):
        details = request.form
        for i in details:
            if(len(details[i])==0):
                flash('Please enter all the details', 'warning')
                return render_template('home.html',data=data)
        tme = time.strftime('%Y-%m-%d %H:%M:%S')
        firstName = details['firstName']
        lastName = details['lastName']
        email = details['email']
        phoneNo = details['phoneNo']
        hostId = details['dropdown']
        if(hostId == '-1'):
            flash('Please choose the host','warning')
            return render_template('home.html',data=data)
        db, cursor = connection()
        rows = cursor.execute('''SELECT * FROM visitor_entry WHERE email = %s and check_out = 0''',(email,))
        if(rows == 0):
            flash('Checked-in successfully', 'info')
            cursor.execute('''INSERT INTO visitor_entry(host_id,first_name,last_name,email,phone_no,check_in) VALUES (%s,%s, %s, %s, %s, %s)''',(hostId,firstName,lastName,email,phoneNo,tme))
            cursor.execute('''SELECT * from host_entry WHERE host_id = %s''',(hostId,))
            details = cursor.fetchone()
            recEmail = details[3]
            number = f"+91{details[4]}"
            try:
                mail = Mail(app)
                msg = Message('Visitor Details', sender = EMAIL_ID, recipients = [recEmail[0]])
                msg.body = f"Name: {firstName} {lastName}\nE-mail: {email}\nPhone: {phoneNo}\nCheck-in: {tme}"
                print(msg.body)
                mail.send(msg)
            except:
                print('Error in test mail')
            try:
                client = getClient()
                message = client.messages \
                    .create(
                        body=f"Name: {firstName} {lastName}\nE-mail: {email}\nPhone: {phoneNo}\nCheck-in: {tme}",
                        from_=TWILIO_NUMBER,
                        to=number
                    )
                print(message.sid)
            except:
                print('Error in SMS client')
            
        
        else:
            flash('You are already checked-in','warning')
        db.commit()
        db.close()
    return render_template('home.html',data=data)




@app.route("/checkout", methods = ['GET','POST'])
def checkout():
    if(request.method == 'POST'):
        details = request.form
        for i in details:
            if(len(details[i])==0):
                flash('Please enter all the details', 'warning')
                return render_template('home.html')
        tme = time.strftime('%Y-%m-%d %H:%M:%S')
        print(tme)
        email = details['email']

        db, cursor = connection()
        rows = cursor.execute('''SELECT * FROM visitor_entry WHERE email = %s and check_out = 0''',(email,))
        if(rows == 0):
            flash('Not checked-in', 'warning')
        else:
            details = cursor.fetchone()
            id = details[0]
            print(id)
            flash('Checked-out successfully', 'info')
            cursor.execute('''UPDATE visitor_entry SET check_out = %s WHERE visitor_id = %s''',(tme,id))
            firstName = details[2]
            lastName = details[3]
            email = details[4]
            phoneNo = details[5]
            checkIn = details[6]
            try:
                mail = Mail(app)
                msg = Message('Visitor Details', sender = EMAIL_ID, recipients = [email])
                msg.body = f"Name: {firstName} {lastName}\nE-mail: {email}\nPhone: {phoneNo}\nCheck-in: {checkIn}\nCheck-out: {tme}"
                print(msg.body)
                mail.send(msg)
            except smtplib.SMTPException:
                print('Error in test mail')
            db.commit()
            db.close()
            return render_template('home.html')
        db.commit()
        db.close()
    return render_template('checkout.html')

@app.route("/history", methods = ['GET','POST'])
def history():
    if(not current_user.is_authenticated):
        flash('Please log in','warning')
        return render_template('login.html')
    id = current_user.get_id()
    db, cursor = connection()
    cursor.execute('''SELECT * FROM visitor_entry WHERE host_id = %s and check_out = 0''',(id,))
    activeData = cursor.fetchall()
    print(activeData)
    cursor.execute('''SELECT * FROM visitor_entry WHERE host_id = %s and check_out != 0''',(id,))
    pastData = cursor.fetchall()
    print(pastData)
    db.close()
    return render_template('history.html', activeData=activeData, pastData=pastData)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if(request.method == 'POST'):
        details = request.form
        for i in details:
            if(len(details[i])==0):
                flash('Please enter all the details', 'warning')
                return render_template('register.html')
        firstName = details['firstName']
        lastName = details['lastName']
        email = details['email']
        phoneNo = details['phoneNo']
        password = bcrypt.generate_password_hash(details['password']).decode('utf-8')
        db, cursor = connection()
        x=cursor.execute('''SELECT * FROM host_entry WHERE email = %s''',(email,))
        if(x == 0):
            flash('Registered successfully', 'info')
            cursor.execute('''INSERT INTO host_entry(first_name,last_name,email,phone_no,password) VALUES (%s, %s, %s, %s, %s)''',(firstName,lastName,email,phoneNo,password))
        else:
            flash('You have already registered','warning')
        db.commit()
        db.close()
        return render_template('login.html')
    return render_template('register.html', title='Register')


@login_manager.user_loader
def load_user(userID):
    db, cursor = connection()
    cursor.execute('''SELECT * FROM host_entry WHERE host_id = %s''',(int(userID),))
    users = cursor.fetchone()
    id= users[0]
    email = users[3]
    password = users[5]
    user = User(id,email,password)
    db.close()
    return user

class User(UserMixin):
    id = 1
    email = ''
    password = ''
    def __init__(self,id,email,password):
        self.id=id
        self.email=email
        self.password=password

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if(request.method == 'POST'):
        details = request.form
        print(details)
        for i in details:
            if(len(details[i])==0):
                flash('Please enter all the details', 'warning')
                return render_template('login.html')
        email = details['email']
        db, cursor = connection()
        x=cursor.execute('''SELECT * FROM host_entry WHERE email = %s''',(email,))
        if(x == 0):
            flash('Account not found', 'warning')
            return render_template('login.html')
        else:
            data = cursor.fetchone()
            id = data[0]
            email = data[3]
            password = data[5]
            if(bcrypt.check_password_hash(password, details['password'])):
                flash('Logged in successfully', 'info')
                user = User(id,email,password)
                login_user(user)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash('Login unsuccessful, please check you email and password', 'warning')
        db.commit()
        db.close()
        return render_template('login.html')
    return render_template('login.html', title='Login')


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)