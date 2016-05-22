from datetime import datetime

from flask import Flask, render_template, request, session, flash

# flask-sqlalchemy also installs and imports sqlalchemy as a requirement
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
# A Secret key that we need to use sessions
app.secret_key = 'asdfhjaksdfh'
# Chooses the file location of the sqlite DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///guestbook.db'
db = SQLAlchemy(app)


# The DB Schema, or model (SQLAlchemy will create the schema based on this)
class GuestBook(db.Model):
    # primary_key=True means that SQLAlchemy will automatically generate
    # IDs for this column and so you never have to touch it.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    message = db.Column(db.Text(500))
    created = db.Column(db.DateTime, default=datetime.utcnow)

    # Creates DB the DB objects that can be saved.
    def __init__(self, name, message):
        self.name = name
        self.message = message


# Explicitly say it can handle both GET and POST now (necessary for POST to work)
@app.route('/', methods=['GET', 'POST'])
def guestbook():
    # If posted to and basic validation on input
    if request.method == 'POST':

        name = request.form['name']
        message = request.form['message']

        error = False
        if not name:
            error = True
            flash('Please provide your name!')
        if not message:
            error = True
            flash('Please provide a message!')
        if 'name' in session:
            error = True
            flash('You already signed the guest book!')

        # Save to DB and session
        if not error:
            session['name'] = name
            entry = GuestBook(name=name, message=message)
            db.session.add(entry)
            db.session.commit()

    # Get all Guest Book Entries and Pass to template
    entries = GuestBook.query.all()
    return render_template('home.html', entries=entries)


if __name__ == '__main__':
    db.create_all()
    app.debug = True
    app.run('0.0.0.0')
