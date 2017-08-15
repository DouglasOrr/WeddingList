import flask
app = flask.Flask(__name__)


@app.route('/')
def welcome():
    return 'The server is running, let\'s go...'
