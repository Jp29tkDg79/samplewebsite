from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
import os

from database import person

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', info='')

    if request.method == 'POST':
        # get data and check data
        username = request.form.get('username')
        password = request.form.get('password')
        info = ''

        if username == '':
            info = 'ユーザ名が未入力です'

        elif password == '':
            info = 'パスワードが未入力です'

        else:
            # create persons object
            persondb = person.persondb()
            # check login data
            match_count = persondb.check_login(username, password)
            if match_count == 1:
                return viewhome(username)
            else:
                info = '登録されていません'

        return render_template('login.html', info=info)

@app.route('/newentry', methods=['GET', 'POST'])
def newuser():
    if request.method == 'GET':
        return render_template('newentry.html', info='')

    if request.method == 'POST':
        # get data and check data
        username = request.form.get('username')
        password = request.form.get('password')
        info =   ''
        if username == '':
            info = 'ユーザ名が未入力です'
        elif 14 < len(username):
            info = 'ユーザ名は14文字内で入力してください'

        elif password == '':
            info = 'パスワードが未入力です'

        elif password != request.form.get('reinptpw'):
            info = '入力したパスワードが異なります 再度入力してください'

        else:
            # create persons object
            persondb = person.persondb()
            # insert data
            err = persondb.insert(username, password)
            if err == '':
                return viewhome(username)
            else:
                info = '既に登録されています'

        return render_template('newentry.html', info=info)

@app.route('/change_pw/<username>', methods=['GET', 'POST'])
def change_pw(username):
    if request.method == 'GET':
        return render_template('change_pw.html', username=username, info='')

    if request.method == 'POST':
        befor_pw = request.form.get('befor_pw')
        after_pw = request.form.get('after_pw')
        info = ''

        if befor_pw == '':
            info = '変更前のパスワードが入力されていません'

        elif after_pw == '':
            info = '変更後のパスワードが入力されていません'

        # check password
        elif after_pw != request.form.get('check_pw'):
            info = '変更後と再確認のパスワードが相違しています'

        else:
            # create person object
            persondb = person.persondb()
            err = persondb.update(username, befor_pw, after_pw)
            if err == '':
                return viewhome(username)
            else:
                info = '変更前のパスワードが誤っています'

        return render_template('change_pw.html', username=username, info=info)


@app.route('/home/<username>', methods=['GET'])
def viewhome(username):
    return render_template('home.html', username=username)

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)

        if filename:
            file_path = os.path.join(app.root_path, endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

def main(debug=False):
    app.run(host='0.0.0.0', port='5000', debug=debug)
