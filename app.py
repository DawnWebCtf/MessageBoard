from flask import Flask, render_template, request, flash, url_for, redirect, session
import os
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

memory = dict(admin="123456")
message = dict()


@app.route("/", methods=['GET', 'POST'])
def index():
    if session.get('uname') != None:
        return render_template("subMessage.html", msgData=message)
    else:
        return redirect(url_for("login"))


@app.route("/subMsg", methods=['POST'])
def subMsg():
    msg = request.form['msg']
    uname = session.get('uname')
    if session.get('count') == 0:
        message[uname] = []
    message[uname].append(msg)
    session['count'] += 1
    flash("留言发表成功")
    return redirect(url_for("index"))


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    elif request.method == 'POST':
        uname = request.form['uname']
        passwd = request.form['passwd']
        if memory.get(uname) != None:
            flash("账号已注册")
            return redirect(url_for("register"))
        else:
            memory[uname] = passwd
            flash("账号注册成功")
            return redirect(url_for("login"))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['uname']
        passwd = request.form['passwd']
        try:
            if memory[uname] == passwd:
                flash("登陆成功")
                session['uname'] = uname
                session['count'] = 0
                return redirect(url_for('index'))
            else:
                flash("登陆失败")
                return redirect(url_for("index"))
        except:
                flash("登陆失败")
                return redirect(url_for("index"))
    return render_template("login.html")

if __name__ == "__main__":
    app.run()
