from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    info = db.Column(db.String(100))
    date = db.Column(db.DateTime, default=datetime.utcnow)

    actor_id = db.Column(db.Integer, db.ForeignKey('actor.id'), primary_key=True)
    actor = db.relationship('Actor', backref=db.backref('movies', lazy=True))

    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'), primary_key=True)
    genre = db.relationship('Genre', backref=db.backref('movies', lazy=True))

    def __repr__(self):
        return '<Movie %r>' % self.id

class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String(100))
    info = db.Column(db.String(100))
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Genre %r>' % self.id

class Actor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    info = db.Column(db.String(100))
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Actor %r>' % self.id

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/movies/<int:id>')
def movie_detail(id):
    movie = Movie.query.get(id)
    return render_template('movie_detail.html', movie=movie)


@app.route('/info_add', methods=['POST', 'GET'])
def create_movie():
    if request.method == 'POST':
        name = request.form['name']
        info = request.form['info']

        movie = Movie(name=name, info=info)

        try:
            db.session.add(movie)
            db.session.commit()
            return redirect('/movies')
        except:
            return 'Error'
    else:
        return render_template('info_add.html')


if __name__ == '__main__':
    app.run(debug=True)