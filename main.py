from crypt import methods
from email.policy import default
from termios import IEXTEN
from flask import (Flask, redirect, render_template, request)
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, default=True)

    def __repr__(self) -> str:
        return self.title


@app.route("/")
def get_main_page():
    items = Item.query.all()
    return render_template("index.html", data=items)


@app.route("/about")
def get_about_page():
    return render_template("about.html")


@app.route("/create-item", methods=["POST", "GET"])
def create_item():
    if request.method == "POST":
        title = request.form["title"]
        text = request.form["text"]
        price = request.form["price"]

        item = Item(title=title, text=text, price=price)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect("/")
        except:
            return "При добавлении товара произошла ошибка!"
    else:
        return render_template("create-item.html")







if __name__ == "__main__":
    app.run(debug=True)