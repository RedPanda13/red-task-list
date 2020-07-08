from flask import Flask
import smtplib
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = "esse troco e chato"

user_email = "redtasklist@gmail.com"
pwd_email = "tasks.31"


client = MongoClient("mongodb+srv://stephan:feichas@cluster0-jyq03.gcp.mongodb.net/usuario?retryWrites=true&w=majority")
db = client.feichas
user = db.usuarios
task = db.tarefas


def send_mail(email, message):
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(user_email, pwd_email )
    server.sendmail(user_email,email, message)
    server.quit()
