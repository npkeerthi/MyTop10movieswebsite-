# installs r down
# api details down


from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from flask_wtf import FlaskForm  
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'lmnopsrt'
Bootstrap(app)


##CREATE DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##CREATE TABLE
class movie(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(50),unique=True,nullable=False)
    year=db.Column(db.Integer,nullable=False)
    description = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(250), nullable=True)
    img_url = db.Column(db.String(250), nullable=False)
db.create_all()


# just for adding atleast one record
record=movie(
    title="Shang Chi",
    year=2021,
    description=" Shang-Chi is forced to confront his past when his father , the leader of the Ten Rings organization, draws Shang-Chi into a search for a mythical village. Martial-arts master Shang-Chi confronts the past he thought he left behind when he's drawn into the web of the mysterious Ten Rings organization.",
    rating=9.8,
    ranking=2,
    review="Technology And Mithology",
    img_url="https://lionstale.org/wp-content/uploads/2021/09/marvel-poster.jpg"
)
# db.session.add(record)
db.session.commit()


@app.route("/")
def home():
                                                             # This line creates a list of all the movies sorted by rating
    allmov=movie.query.order_by(movie.rating).all()
    print(allmov)
    for i in range(len(allmov)):
        allmov[i].ranking=len(allmov)-i
        print(allmov[i].ranking)
    db.session.commit()
    return render_template("index.html",movies=allmov)

class ratemovieform(FlaskForm):
    rating=StringField("Your Rating Out Of 10")
    review=StringField("Your Review")
    submit=SubmitField("Update")                          #this goes in edithtml as wtf form

@app.route("/edit",methods=["GET","POST"])
def editinfo():
    form=ratemovieform()
    muv_id=request.args.get("id")
    muv=movie.query.get(muv_id)
    if form.validate_on_submit():
        muv.rating=float(form.rating.data)
        muv.review=form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html",moviee=muv,formm=form)



@app.route("/delete")
def delete():
    del_id=request.args.get('record_id')
    print("del id: ",del_id)

    tobedel=movie.query.get(del_id)
    db.session.delete(tobedel)
    db.session.commit()
    return redirect(url_for('home'))




class addmovieform(FlaskForm):
    movietitle=StringField("Movie Title",validators=[DataRequired()])
    button=SubmitField("Add Movie")


MOVIE_DB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
mdbinfo_url="https://api.themoviedb.org/3/movie"
mdb_img_url="https://image.tmdb.org/t/p/w500"
key="04077d96563d130ce2136dfccfea2605"


@app.route('/add',methods=["GET","POST"])
def addmovie():
    addingform=addmovieform()
    if addingform.validate_on_submit():
        movie_title=addingform.movietitle.data

        resp=requests.get(
            MOVIE_DB_SEARCH_URL,params={'api_key':key,"query":movie_title} )
        resdata=resp.json()["results"]
        return render_template("select.html",options=resdata)

    return render_template("add.html",aform=addingform)



@app.route("/find")
def findmovie():
    movie_api_id = request.args.get("ID")
    if movie_api_id:
        movie_api_url = f"{mdbinfo_url}/{movie_api_id}"

        response=requests.get(movie_api_url,params={"api_key":key,"language":"en-US"})
        data=response.json()

        thatmovie=movie(
            title=data["title"],
            year=data["release_date"].split("-")[0],
            img_url=f"{mdb_img_url}{data['poster_path']}",
            description=data["overview"]
        )
        db.session.add(thatmovie)
        db.session.commit()
        return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(debug=True)













# pip install flask_sqlalchemy    pip install sqlalchemy==1.3.23
#pip install Flask-Bootstrap4
# pip install flask-wtf

# API Key (v3 auth)
# 04077d96563d130ce2136dfccfea2605
# Example API Request
# https://api.themoviedb.org/3/movie/550?api_key=04077d96563d130ce2136dfccfea2605
# API Read Access Token (v4 auth)
# eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIwNDA3N2Q5NjU2M2QxMzBjZTIxMzZkZmNjZmVhMjYwNSIsInN1YiI6IjYxZmU4ODUxY2I3MWI4MDA5NDMyZTdkZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.eNyaPfY7sew8NmFFolCEwmhIM7173sBjGGRTvk8m8NI

