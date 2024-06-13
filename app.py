# importing the libraries needed for the project
import psycopg2
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

# Initialise the App
app = Flask(__name__)


ENV = 'dev'

if ENV == 'dev':
  app.debug = True
  app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/db_duncan"


else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
app.app_context().push()

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    dealer =db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self,customer, dealer, rating, comments):
        self.customer = customer
        self.dealer = dealer
        self.rating = rating
        self.comments = comments


# creating the routes 
@app.route('/')
def land():
    return render_template('landing.html')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit',methods=['POST'])

def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        dealer = request.form['dealer']
        rating = request.form['rating']
        comments = request.form['Comments']
        print(customer,dealer,rating,comments)
        if customer == '' or dealer == '':
           return render_template('index.html',message='Please enter the required fields')
        if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
            data = Feedback(customer, dealer, rating, comments)
            db.session.add(data)
            db.session.commit()
            return render_template('success.html')
        return render_template('index.html', message='You Have already submitted feedback')



if __name__ == '__main__':
    app.run()
