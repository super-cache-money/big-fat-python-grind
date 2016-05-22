from flask import Flask
app = Flask(__name__)


@app.route('/<name>')
def hello(name):
    return 'Hello {}, my name is ...'.format(name)

if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0')
