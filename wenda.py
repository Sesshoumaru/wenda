from flask import Flask, render_template, request, url_for, redirect, session
import config
from extensions import db
from models import User, Question, Answer
from decorators import login_required
from sqlalchemy import or_
app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route("/")
def index():
    context = {
        'questions': Question.query.order_by('-createtime').all()
    }
    return render_template("index.html", **context)


@app.route("/search/")
def search():
    q = request.args.get("q")
    condition = or_(Question.title.contains(q),Question.content.contains(q))
    context = {
        'questions': Question.query.filter(condition).order_by('-createtime').all()
    }
    return render_template("index.html", **context)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get("telephone")
        password = request.form.get("password")

        user = User.query.filter(User.telephone == telephone,).first()

        if user and user.check_password(password):
            session["user_id"] = user.id
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return "用户名不存在，或者密码错误!"

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


@app.route("/question/", methods=["GET", "POST"])
@login_required
def question():
    if request.method == "GET":
        return render_template("question.html")
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        user_id = session.get("user_id")

        question = Question(title=title, content=content)
        question.author_id = user_id
        db.session.add(question)
        db.session.commit()

        return redirect(url_for('index'))


@app.route("/detail/<question_id>")
def detail(question_id):
    question_model = Question.query.filter(Question.id == question_id).first()
    return render_template('detail.html', question=question_model)


@app.route("/add_answer/", methods=['POST'])
@login_required
def add_answer():
    content = request.form.get('answer_content')
    question_id = request.form.get('question_id')
    user_id = session.get('user_id')
    answer = Answer(content=content)
    answer.question_id = question_id
    answer.author_id = user_id
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('detail', question_id=question_id))


@app.before_request
def my_before_requset():
    print('my_before_requset: ',request.url)
    pass;



@app.context_processor
def my_context_processor():
    print('my_context_processor: ',request.url)

    user_id = session.get("user_id")
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {"user": user}

    return {}


if __name__ == "__main__":
    app.run()
