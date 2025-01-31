import sys
from flask import Flask, request, render_template, session, redirect, url_for
from flask.views import MethodView
from flask_restful import Api, Resource
import mysql.connector as mydb
import hashlib

sys.path.append("/home/")
from ml.model_api import Predictor
#from ml.fake_model_api import Predictor

app = Flask(__name__)
api = Api(app)
app.secret_key = b"hogefugahoge" #TODO
salt = "masakick" #TODO

member_data = {} #TODO


class LoginAPI(MethodView):
    def get(self):
        return render_template("login.html")

    def post(self):
        # コネクションの作成
        conn = mydb.connect(
            host='db_server',
            port='3306',
            user='root',
            password='masakick',
            database='testdb'
        )
        global member_data
        name = request.form.get("id", "", type=str)
        _pass = request.form.get("pass", "", type=str) + salt
        _pass = hashlib.sha512(_pass.encode("utf-8")).hexdigest()
        cur = conn.cursor()
        cur.execute("select pass from members where name = '%s'"%name)
        res = cur.fetchone()
        if res is None:
            #TODO
            session["login"] = True
            cur.execute("insert into members values ('%s', '%s')"%(name, _pass))
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for("index"))
        else:
            if res[0] == _pass:
                session["login"] = True
            else:
                session["login"] = False
        """
        if name in member_data:
            if _pass == member_data[name]:
                session["login"] = True
            else:
                session["login"] = False
        else:
            member_data[name] = _pass
            session["login"] = True
        """
        cur.close()
        conn.close()
        session["id"] = name
        if session["login"]:
            return redirect(url_for("index"))
        else:
            return render_template("login.html")

class MainAPI(MethodView):
    def get(self):
        if session.get("login") is None or not session["login"]:
            return redirect(url_for("login"))
        if "text" in session:
            text = session["text"]
            pred = session["pred"]
        else:
            text = ""
            pred = ""
        return render_template("main.html", result=pred, text=text)

    def post(self):
        text = request.form.get("text", "", type=str)
        lang = request.form.get("lang", "jap", type=str)
        session["text"] = text
        predictor = Predictor(lang=lang)
        pred = predictor.predict(text, lang=lang)
        session["pred"] = pred
        return redirect(url_for("index"))

class Logout(MethodView):
    def get(self):
        session.pop("id", None)
        session.pop("login")
        if "text" in session:
            session.pop("text")
            session.pop("pred")
        return redirect(url_for("login"))

app.add_url_rule("/login/", endpoint="login",  view_func=LoginAPI.as_view("login"))
app.add_url_rule("/", endpoint="index", view_func=MainAPI.as_view("hoge"))
app.add_url_rule("/logout/", endpoint="logout", view_func=Logout.as_view("logout"))


if __name__ == '__main__':
    app.run()
    #app.run(debug = True, host="0.0.0.0") #TODO
