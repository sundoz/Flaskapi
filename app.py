from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///baza.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key = True) # тип и уникальность
    title = db.Column(db.String(100), nullable=False) # тип длина и возможность нулевого(пустого значения
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return '<Note %r>' %self.id


@app.route('/')
@app.route('/home')
def index():
    return render_template("Index.html")


@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/posts')
def posts():
    articles = Note.query.order_by(Note.date).all()
    return render_template('posts.html', articles=articles)



@app.route('/note', methods=['POST', 'GET'])
def note():
    if request.method == 'POST':

        title = request.form['title']
        intro = request.form['intro']
        text= request.form['text']

        notes = Note(title=title, intro=intro, text=text)
        try:

            db.session.add(notes)
            db.session.commit()
            return redirect('/')
        except:
            return "ERROR"
    else:
         return render_template('note.html')
