# Flask
Flask is a micro web framework, which means that it only comes with the bare minimum you need to write a minimal web application, which allows it to have the least amount of boiler plate possible, stay light weight and avoid unnecessary baggage. More features are added via extensions, which are usually curated to ensure quality and consistency.
 
This means that when your project grows larger and more complex, then you have multiple choices as to what extensions you can use to achieve the same goal and multiple ways to structure your application to suit your needs. This means that flask is **un-opinionated**

However the disadvantage of this is that there is more decision making required on the part of the developer and on-boarding for new developers takes longer, as any two projects could have a very different set of extensions and structure.

This is in contrast to a full web framework like Django, which gives you a structure and all the features that you would need to make a full web application out of the box (which is what 'batteries included' means).

Flask only includes what you would definitely want to have for any web page, Which is a templating system (Jinja2), session and cookie handling and a few defaults like a static file path, a development server and a few other features that almost every web app would use. Things that Flask doesn't include but Django does, is among other things an ORM (for databases), user management and configuration files already set up in a specific way.

## Installation
You can install Flask by using pip, by simply typing ```pip install flask``` in your terminal to install it to your global site packages (your operating system's python packages) or ```pip3 install flask``` in order to make sure that you install it for your Python 3's site packages, as different versions of Python can have their own separate site packages.
Alternatively, if you are using Pycharm, you can just use Pycharm to do this for you. Go to ```Settings -> Project: <Project Name> -> Project Interpreter``` and click on the green plus symbol to then find and install flask that way.

## Hello World
```python
from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, my name is ...'

if __name__ == '__main__':
    app.run()
```
This is a very basic hello world app that you can run and browse to in your browser thanks to Flask's built in development server. By default the port is **5000**, so you can reach your page at ```http://127.0.0.1:5000```. Note that the development server should also automatically detect changes in your python files and automatically restart itself.

To make the page accessible outside of your system (to other people on the network), replace ```app.run()``` with ```app.run('0.0.0.0')```.

To enable a debug console on your page that comes up when there is an error, then you can also add ```app.debug = True``` in the last if statement but before the ```.run()``` method. So for example, you can deliberately add a failing assert statement in order to give us an excuse to explore our running code in the browser, so for example we can do something like this to apply all of the above:
```python
from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello():
    assert 1 == 2
    return 'Hello, my name is ...'

if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0')
```
Note that the debug console is protected by a pin that you will get when you launch your flask app.

Finally, note that although the Flask production server can be used to publish your site on the web, you should'nt do it as it can only handle one request at a time and is insecure. What you would normally use is a different web server like **gunicorn** and a proxy server like **nginx**, or alternatively a deployment environment like Heroku or Google App Engine which can handle that for you.

## What's going on
The object that we assigned to```app``` is what is called the **application context**, which is basically the object representing a specific instance of Flask. It contains all the information that flask and it's extensions need to handle requests and know which Flask application instance to work with.

### Routing
```@app.route('/')``` is a Flask **decorator** that tells Flask which urls and HTTP methods route to which functions, with the first parameter being the path you want function to listen for. So we can change it to ```'/hello'``` to make us have to go to ```http://127.0.0.1:5000/hello``` instead. By default, it only listens to HTTP **GET** methods, but we can specify which methods it accepts by passing in the optional keyword argument ```methods```, so for example the following is the equivalent of the default behaviour:
```python
@app.route('/', methods=['GET'])
```
and the following accepts bot **GET** and **POST** methods:
```python
@app.route('/', methods=['GET', 'POST'])
```

### Variable Routing
 If you have parts of your URL that are variables, then you can handle those URLs and the variables in that URL by doing the following:
```python
@app.route('/<name>')
def hello(name):
    return 'Hello {}, my name is ...'.format(name)
```
So what is happening here is that the route extracts the text in the parts of the URL that you specify with the ```<``` and ```>``` characters and passes them into the function as keyword arguments where the keyword is the name in those characters (EG: ```name``` above). You can have multiple variables in your URL as long as they are matched by what the number and names of your arguments are in the function below it.

## Task
The goal of this task is simply to make sure your app is running and accessible and to determine your system's IP address so that you can show your site to other people in the tutorial for later tasks:
- Serve a **functioning** flask app that accepts a user's name as a variable URL, greets the user (similar to the example above) and also displays your name as the 'greeter (i.e: Hello [user's name], my name is [your name here]).
- Make sure that it is publicly accessible
- Tell the tutor your system's IP address (it can be found with the ```ifconfig``` console command in linux and OSX or ```ipconfig``` in Windows).