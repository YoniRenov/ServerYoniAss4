from flask import Flask, redirect, render_template
from flask import url_for
from flask import render_template, blueprints
from datetime import timedelta
from flask import request, session, jsonify

app = Flask(__name__)
app.secret_key = '123'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=40)

from assignment_4.assignment_4 import assignment_4

app.register_blueprint(assignment_4)

user_dict = {
    'Yehonatan Renov': ['Yehonatan@gmail.com', '115599', 'Yehonatan', 'Renov', '26', 'Beer-Sheva', 'Kevin De Bruyne'],
    'Gaston Kirsman': ['Gasti@gmail.com', '775533', 'Gaston', 'Kirsman', '27', 'Tel Aviv', 'Raheem Sterling'],
    'Ariel Warren': ['Ariel@gmail.com', '774411', 'Ariel', 'Warren', '28', 'Jerusalem', 'Kyle Walker'],
    'Maayan Amos': ['Maayan@gmail.com', '885522', 'Maayan', 'Amos', '24', 'Tel Aviv', 'Aymeric Laporte'],
    'Aviya David': ['Aviya@gmail.com', '996633', 'Aviya', 'David', '29', 'Ashdod', 'Erling Haaland'],
    'Enas Hallak': ['Enas@gmail.com', '445566', 'Enas', 'Hallak', '23', 'Fasuta', 'Joel Cancello']
}


@app.route('/')
def getHomepage():
    return render_template('HomePage.html')


@app.route('/contact')
def getContactpage():
    return render_template('Contact.html')


@app.route('/assignment3_1')
def getassignment3_1():
    user_info = {'First Name:': 'Yehonatan', 'Last Name:': 'Renov', 'Gender': 'Male', 'Age:': '26',
                 'City:': 'Beer-Sheva'}
    hobbies = ('football', 'basketball', 'books', 'food', 'sea')
    films = ('Avengers: End Game', 'Captain America', 'Iron Man 2')
    musicArtists = ('black eyed peas', 'avici', 'akon')
    return render_template('assignment3_1.html',
                           user_info=user_info,
                           hobbies=hobbies,
                           films=films,
                           musicArtists=musicArtists)


@app.route('/session')
def session_func():
    # print(session['CHECK'])
    return jsonify(dict(session))


@app.route('/assgnment3_2', methods=['GET', 'POST'])
def Assignment3_2():
    if request.method == 'POST':

        reg_Username = request.form['user_name']
        reg_UserEmail = request.form['user_email']
        reg_Firstname = request.form['user_Firstname']
        reg_Lastname = request.form['user_Lastname']
        reg_Age = request.form['user_age']
        reg_City = request.form['user_City']
        reg_FavPlayer = request.form['user_FavPlayer']
        reg_password = request.form['user_pass']

        session['user_Name'] = reg_Username
        session['user_Email'] = reg_UserEmail
        session['user_Firstname'] = reg_Firstname
        session['user_Lastname'] = reg_Lastname
        session['user_Age'] = reg_Age
        session['user_City'] = reg_City
        session['user_FavPlayer'] = reg_FavPlayer
        session['user_password'] = reg_password
        session['Registered'] = True
        if reg_Username in user_dict:
            return render_template('assgnment3_2.html', message2='You already registered !')
        else:
            new_user = {reg_Username: [reg_UserEmail, reg_password, reg_Firstname, reg_Lastname, reg_Age, reg_City,
                                       reg_FavPlayer]}
            user_dict.update(new_user)
            return render_template('assgnment3_2.html', message2='Successfully Registered ! Welcome to the Club!')
        return render_template('assgnment3_2.html')

    if request.method == 'GET':
        if 'user_Name' in request.args:
            user_name = request.args['user_Name']
            if user_name in user_dict:
                return render_template('assgnment3_2.html',
                                       user_Name=user_name,
                                       user_Email=user_dict[user_name][0],
                                       user_Firstname=user_dict[user_name][2],
                                       user_Lastname=user_dict[user_name][3],
                                       user_Age=user_dict[user_name][4],
                                       user_City=user_dict[user_name][5],
                                       user_FavPlayer=user_dict[user_name][6]
                                       )
            elif len(user_name) == 0:
                return render_template('assgnment3_2.html',
                                       user_dict=user_dict)

            else:
                return render_template('assgnment3_2.html',
                                       message='User not found.')
    return render_template('assgnment3_2.html')


@app.route('/log_out')
def logout():
    session['Registered'] = False
    session.clear()
    return redirect(url_for('Assignment3_2'))


if __name__ == '__main__':
    app.run()
