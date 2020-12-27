import os
from PIL import Image
from datetime import datetime
from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///artikel.db'
app.config["IMAGE_UPLOADS"] = "D:\Project\ESD\Forum Literasi\static\image"
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    judul = db.Column(db.String(200), nullable = False)
    kategori = db.Column(db.String(50), nullable = False)
    isi_artikel = db.Column(db.String(1500), nullable = False)
    penulis = db.Column(db.String(50), nullable = False)
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, judul, kategori, isi_artikel, penulis):
        self.judul = judul
        self.kategori = kategori
        self.isi_artikel = isi_artikel
        self.penulis = penulis

@app.route("/")
def index():
    data = Todo.query.order_by(Todo.date_created).all()
    return render_template("index.html", data = data)

@app.route("/admin")
def admin():
    data = Todo.query.order_by(Todo.date_created).all()
    return render_template("admin.html", data = data)

@app.route("/create", methods = ['POST', 'GET'])
def create():
    if request.method == "POST":
        if request.files:
            input_judul = request.form['judul']
            input_penulis = request.form['nama_penulis']
            input_kategori = request.form['kategori'].title()
            input_artikel = request.form['artikel']
            input_data = Todo(input_judul, input_kategori, input_artikel, input_penulis)
            image = request.files['image']
            if image.filename == "":
                return "There is no image to be uploaded"
            try:
                db.session.add(input_data)
                db.session.commit()
                image.filename = str(input_data.id) + ".png"
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
                return redirect('/')
            except:
                return "There was problem when inserting new data"
    else:
        return render_template("create.html")

@app.route("/delete/<int:id>")
def delete(id):
    data = Todo.query.get_or_404(id)
    try:

        db.session.delete(data)
        db.session.commit()
        os.remove('static/image/{}.png'.format(id))
        return redirect('/')
    except:
        return 'There was a problem in deleting data'

@app.route("/update/<int:id>", methods = ['GET', 'POST'])
def update(id):
    data = Todo.query.get_or_404(id)
    if request.method == "POST":
        data.judul = request.form['judul']
        data.penulis = request.form['nama_penulis']
        data.kategori = request.form['kategori'].title()
        data.isi_artikel = request.form['artikel']
        data.date_created = datetime.now()
        db.session.commit()
        return redirect("/")
    else:
        return render_template("update.html", data = data)

@app.route("/article/<int:id>-<judul>")
def article(id, judul):
    data = Todo.query.get_or_404(id)
    return render_template("article.html", data = data)

@app.route("/category")
def category():
    return render_template("category.html")

@app.route("/category/<name>")
def detail_category(name):
    if name != "User-Interface User-Experience":
        name = " ".join(name.split("-"))
    data = Todo.query.filter(Todo.kategori == name).all()
    return render_template("detail_category.html", data = data, name = name)

@app.route("/about-us")
def about_us():
    return render_template("about_us.html")

@app.route("/author/<penulis>")
def author_article(penulis):
    data = Todo.query.filter(Todo.penulis == penulis).all()
    return render_template("author_article.html", data = data, name = penulis)

@app.route("/login")
def login():
    return render_template("login.html")
if __name__ == "__main__":
    app.run(debug=True)