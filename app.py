from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import hashlib

app = Flask(__name__)

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = hash_password(request.form['password'])

        try:
            conn = sqlite3.connect('./src/data/users.db')
            c = conn.cursor()
            c.execute(
                'INSERT INTO users (username, password) VALUES (?, ?)',
                (username, password)
            )
            conn.commit()
            conn.close()
            return "注册成功 <a href='/login'>请登录</a>"
        except sqlite3.IntegrityError:
            return '用户名已存在'
    else:
        return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = hash_password(request.form['password'])

        conn = sqlite3.connect('./src/data/users.db')
        c = conn.cursor()
        c.execute(
            'SELECT * FROM users WHERE username = ? AND password = ?',
            (username, password)
        )
        user = c.fetchone()
        conn.close()

        if user:
            return f"登录成功！欢迎 {username}"
        else:
            return "用户名或密码错误"

    return render_template('login.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5050, debug=True)