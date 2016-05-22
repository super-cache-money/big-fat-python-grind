# Flask Guest Book
What we are going to introduce the tools you need to accept and store user data.

## Templates
You can't go far with web development if you just return a basic string to the user, so what we need to do is serve HTML documents to the user and it is much easier to manage these documents if they are in their own separate files that your flask app could just point to.

In order to use templates in flask, first make sure you import ```render_template``` from ```flask```, i.e:
```python
from flask import Flask, render_template
```
Then, in your functions (which we will call **views**) that generate a web page, make sure that you return it like so ```render_template('home.html)```, where `home.html` can be whatever you want to call your html file. By default, flask looks for these files in a folder called ```templates``` in the root of your flask app's directory, so you can just make that folder and put them there.

So to start off with, we can make a very basic HTML called `home.html` file that only says 'hello' and put it in there:
```html
<!DOCTYPE html>
<html>
  <head>
    <title>Guest Book</title>
  </head>
  <body>
    <p>hello!</p>
  </body>
</html>
```

## Submitting (POSTing) user data
In order to let users interact with our page and give us data that we can work with later, we will need to let them **POST** data, which is basically what a web form does. So let's make an HTML form that will POST some data to our site:
```HTML
<!DOCTYPE html>
<html>
  <head>
    <title>Guest Book</title>
  </head>
  <body>

    <form method="post">
      <fieldset>
        <legend>Sign the guest book</legend>
        <div>
          <label>Name:</label>
          <input type="text" name="name" value="">
        </div>
        <div>
          <label>Message:</label>
          <textarea name="message"></textarea>
        </div>
        <div>
          <input type="submit" value="Submit">
        </div>
      </fieldset>
    </form>

  </body>
</html>
```
Then in our Flask app, we must tell our view to accept the POST from our form by adding it as a valid method:
```python
@app.route('/', methods=['GET', 'POST'])
```
To be clear, when our user just goes to our site, it is called a **GET** method, which is when our site gives the HTML to the user's browser to show it's user the page, whereas a **POST** is when the user includes data in their request intended to update something on our site. Our flask view will handle both cases with the same function.
So in order to know which the user is doing (GET or POST), we will need flask's ```request``` object.
In order to use it, first import it from flask, which so far would make our import statement look like this:
```python
from flask import Flask, render-template, request
```
Then in our view, we can inspect the user's request method by simply checking that attribute (```request.method```), which we check in order to do something different if the user POSTs data, like let's say save data to a DataBase:
```python
if request.method == 'POST':
    Do Something
```
Then, to get data from that POST, you can also just use the request object, like so:
```python
name = request.form['name']
message = request.form['message']
```
Note that we got the names of the form data from the `name` attributes in the `input` and `textarea` fields in the HTML above, which is how you refer to form data. 

## Session
What we are going to do now is temporarily store some of the data that the user gave us. The flask ```session``` object stores whatever data we want on the client's browser using what are called **Cookies**. A server makes cookies and gives it to the user's browser to store and then every time the user makes a subsequent request, their browser sends back those same cookies. This means that you don't want to keep the data as small as possible as it will be extra baggage on each request. Cookies are also not meant to be permanent, with cookies usually expiring when the user closes their browser or after a specified period of time.

All this means that what you store in session data should be something temporary and specific to that user's 'session', like log in details or some kind of configuration.
Flask also signs it's cookies with a secret that you specify in order to make sure that only it can make these cookies so as to prevent people making fake cookies and pretending to be a different user for example.

In order use sessions, we must first import the session object:
```python
from flask import FLask, render_template, request, session
```
Then specify our custom secret key (Remember, if anyone sees this key, then your site will be compromised, due to negating the earlier mentioned cookie signing feature):
```python
app.secret_key = 'Super Secret Key!'
```
You can just think of a session as a dictionary the persists between requests, so we simply store data like so:
```python
session['name'] = name
```
And get data like so:
```python
name = session['name']
```
In the next section we will learn how we can present dynamic content like this to the user.

## Jinja2
The point of using a web application instead of a static HTML page is to serve up a **dynamic** web page that changes to fulfill the user's needs. In order to make our HTML pages dynamic, we are going to use Jinja2.

Jinja2 is a templating language which understands and uses Python objects and data types, which allows you to modify and even generate HTML code from within the HTML file on the server before sending it to the client.

Jinja2 comes with flask and is already configured, so you can go straight ahead and start using it in your HTML files. To display a variable, you must use the following notation:
```html
{{ variable_name }}
```
You can get variables into the template by passing them as keyword arguments to the ```render_template``` function, like so:
```python
return render_template('home.html', message='hello')
```
Then in your template you can use it like so:
```html
{{ message }}
```
Which will look like this to the user:
```
hello
```
In addition to explicitly sending objects like that to the template, Flask also implicitly sends the following objects as well: ```request``` and ```session``` which we covered above, ```g``` (a global variable which we will cover later) and ```get_flashed_messages()``` function which we will cover just now.
So for example, you could see everything that is stored in your session by simply doing the following:
```html
{{ session }}
```
and you can access items in your session with dot notation (also, you won't get a key error if the key does not exist):
```html
{{ session.user }}
```

We can also do basic control flow and statements such as if-else and for loops like so:
```html
{% if 'name' in session %}
  <strong>Hello {{ session.name }}</strong>
{% else %}
  <strong>Please sign my Guest Book!</strong>
{% endif %}
```
```html
{% for entry in entries %}
  <p>{{ entry.name }} - {{ entry.message }} - {{ entry.created }}</p>
  <br>
{% endfor %}
```
So ```{% ... %}``` are for Statements (including control flow), ```{{ ... }}``` are for expressions (like variables) and ```{# ... #}``` are for comments.

Jinja2 has a huge amount of features, including macros, which can significantly reduce the amount of HTML that you have to write. You can see it's documentation [here](http://jinja.pocoo.org/docs/dev/templates/).

So here is a full example using everything that we learned so far that allows us to remember and display the user's name for the entire session:
Flask app:
```python
from flask import Flask, render_template, request, session


app = Flask(__name__)
# A Secret key that we need to use sessions
app.secret_key = 'asdfhjaksdfh'


# Explicitly say it can handle both GET and POST now (necessary for POST to work)
@app.route('/', methods=['GET', 'POST'])
def guestbook():
    # If posted to and basic validation on input
    if request.method == 'POST':
        name = request.form['name']
        if name:
            session['name'] = name

    return render_template('home.html')


if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0')
```
```templates/home.html```:
```html
<!DOCTYPE html>
<html>
  <head>
    <title>Guest Book</title>
  </head>
  <body>

    {% if 'name' in session %}
      <strong>Hello {{ session.name }}</strong>
    {% else %}
      <strong>Please sign my Guest Book!</strong>
    {% endif %}

    <form method="post">
      <fieldset>
        <legend>Sign the guest book</legend>
        <div>
          <label>Name:</label>
          <input type="text" name="name" value="">
        </div>
        <div>
          <label>Message:</label>
          <textarea name="message"></textarea>
        </div>
        <div>
          <input type="submit" value="Submit">
        </div>
      </fieldset>
    </form>

  </body>
</html>
```

## Adding a database (SQLAlchemy)
Almost every respectable web application needs to use a database and our Guest Book application is no different, as even though we can remember session data for a specific user, we want to store it permanently and make the data visible to other users.
For this we will use a very simple and lightweight database called **SQLite** and create it's file and interact with it using a very popular Python **ORM** called **SQLAlchemy**.

### Installation
Installation is identical to how we installed Flask. Either user ```pip install flask-sqlalchemy```, ```pip3 install flask-sqlalchemy``` or use Pycharm: ```Settings -> Project: <Project Name> -> Project Interpreter```.

### Implementing it
Flask-SQLAclhemy is a Flask extension that sets up SQLAlchemy for us and so allows us to skip almost all of the boiler plate. To setup our database, we first have to import it:
```python
from flask.ext.sqlaclemy import SQLAlchemy
```
Then we have to point it to a database file (don't worry if it doesn't exist yet as SQLAlchemy will create it automatically for us later):
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///guestbook.db`
```
Then we want a database connection and connect it to our flask app:
```python
db = SQLAlchemy(app)
```
And now we can define our model, which is basically how SQLAlchemy understands our database table:
```python
class GuestBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    message = db.Column(db.Text(500))

    def __init__(self, name, message):
        self.name = name
        self.message = message
```
So what we have going on here, is that there are three columns: 
- **id**, which is an Integer and the Primary Key, which means that it is used to uniquely identify each and every row and will be automatically generated by SQLAclhemy when a row is created and ensured to be unique
- **name**, which is a String of a maximum length of 80 characters and is unique, which means that SQLAlchemy will not allow two rows with the same name columns to exist together in the database 
- **message**, which is a Text field that is more permissive string that we gave a maximum length of 500 characters.
Then we have a constructor (```__init__```) that allows us to automate the creation of rows.

As a bonus, we can also have a column that automatically gets a creation date for the row. First import datetime, which is what will give us the date:
```python
from datetime import datetime
```
Then add the column:
```python
created = db.Column(db.DateTime, default=datetime.utcnow)
```
Now every time that we add a new entry, a **created** row will be added that will automatically get the default value of the date and time on which it was created.

Finally, in order to initialize the database and create the SQLite file if it doesn't already exist, we will add ```db.create_all()``` to the end of our flask app, under the ```if__name__ == '__main__':``` statement, like so:
```python
if __name__ == '__main__':
    db.create_all()
    app.debug = True
    app.run('0.0.0.0')
```

### Using it
In order to put something to the database, we first have to create an object of our model class that we defined above with the help of our constructor:
```python
entry = GuestBook(name=name, message=message)
```
Then we add it to our database:
```python
db.session.add(entry)
```
And then if there are no other database operations that we need to do, we can commit the changes to the database all in one go:
```python
db.session.commit()
```
And that's it.

In order to get all our entries, we can get a query like so:
```python
entries = GuestBook.query.all()
```
And that contains all the rows in our GuestBook table, which we can also pass straight to Jinja2 as a parameter and iterate through, like so:
```python
return render_template('home.html', entries=entries)
```
```templates/home.html```:
```html
    {% if entries %}
      {% for entry in entries %}
        <p>{{ entry.name }} - {{ entry.message }} - {{ entry.created }}</p>
        <br>
      {% endfor %}
    {% else %}
      <p>No existing guest book entries</p>
    {% endif %}
```

You can also filter for a specific entry like so:
```python
admin = GuestBook.query.filter_by(name='admin').first()
```
Which will also return the first row that satisfies the query.

You can also order a query:
```python
entries = GuestBook.query.order_by(GuestBook.name)
```

This is a very basic usage of a SQLAclhemy, which is a very powerful, widely used and fast database ORM.
You can read more about using it in Flask [here](http://flask-sqlalchemy.pocoo.org/2.1/).

## Flash messages
Every web application needs, or at least should give the feedback on their actions and as such, Flask includes a messaging system called **Flash**, which makes it a very easy affair to make messages that will be given to the user on the next response and be automatically cleaned up once the user has seen it and flask also makes these messages available directly in the Jinja2 templates.
 
 To use it, first import it like so (you don't need everything else, as all the other imports are just what we have used so far for this project):
```python
 from flask import Flask, render_template, request, session, flash
```
 Then simply call the flash function from wherever you need it in your flask app as many times as you like with as many different messages as you like:
```python
flash('Please provide your name!')
```
And then flask will make all the flash messages available in a your templates via the function ```get_flashed_messages()```, which will return a list of all the flash messages that the user hasn't seen yet, which you can use in your template like so:
```html
    {% for flash in get_flashed_messages() %}
      <p><strong>{{ flash }}</strong></p>
    {% endfor %}
```

There are some other features, like different categories for flash messages, like errors, warnings or successes. You can read more about flask message flashing [here](http://flask.pocoo.org/docs/0.10/patterns/flashing/).

## Full application example
And here is our app.py file that uses all of the features that we covered unil now:
```python
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
```
And the accompanying template file ```home.html``` located in the ```templates``` folder:
```html
<!DOCTYPE html>
<html>
  <head>
    <title>Guest Book</title>
  </head>
  <body>

    {% if 'name' in session %}
      <strong>Hello {{ session.name }}</strong>
    {% else %}
      <strong>Please sign my Guest Book!</strong>
    {% endif %}

    {% for flash in get_flashed_messages() %}
      <p><strong>{{ flash }}</strong></p>
    {% endfor %}

    <form method="post">
      <fieldset>
        <legend>Sign the guest book</legend>
        <div>
          <label>Name:</label>
          <input type="text" name="name" value="">
        </div>
        <div>
          <label>Message:</label>
          <textarea name="message"></textarea>
        </div>
        <div>
          <input type="submit" value="Submit">
        </div>
      </fieldset>
    </form>

		<br>
		<hr>
		<br>

    {% if entries %}
      {% for entry in entries %}
        <p>{{ entry.name }} - {{ entry.message }} - {{ entry.created }}</p>
        <br>
      {% endfor %}
    {% else %}
      <p>No existing guest book entries</p>
    {% endif %}

  </body>
</html>
```

## Resource
A very useful resource is the online guide called **Explore Flask**, which can be found [here](https://exploreflask.com/en/latest/preface.html).

## Task
Your task is to take your task 2 from day 1 of this Python tutorial, and make it a web based competitive game.
You will be required to:
- Publicly accessible web page that allows users to play [mastermind](https://en.wikipedia.org/wiki/Mastermind_(board_game))
- Track the user and their guesses in a session
- Once they find the correct answer, save the user's name, score and date they completed it to the database and display those results to other users sorted by the highest scorers or date.