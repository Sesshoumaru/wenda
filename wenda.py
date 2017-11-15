from flask import Flask, render_template, request, url_for, redirect, session
import config
from extensions import db
from models import User

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get("telephone")
        password = request.form.get("password")

        user = User.query.filter(User.telephone == telephone, User.password == password).first()
        if not user:
            return "用户名不存在，或者密码错误!"
        else:
            session["user_id"] = user.id
            session.permanent = True
            return redirect(url_for('index'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form.get("username")
        telephone = request.form.get("telephone")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user = User.query.filter(User.telephone == username).first()
        if user:
            return "该手机号码已注册，请更换手机号码!"
        elif password1 != password2:
            return "两次输入的密码不一致，请重新输入!"
        else:
            user = User(username=username, telephone=telephone, password=password1)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))

        return render_template('register.html')



@app.route("/logout/")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.context_processor
def my_context_processor():
    user_id = session.get("user_id")
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {"user":user}

    return {}

if __name__ == "__main__":
    app.run()
