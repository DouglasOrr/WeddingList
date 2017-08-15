import flask
app = flask.Flask(__name__)


@app.route('/')
def root():
    return 'Root page'


@app.route('/items')
def list():
    return 'Wedding list'


@app.route('/items/<int:id>/detail')
def detail(id):
    return 'Detail for %d' % id


@app.route('/items/<int:id>/claim', methods=['POST'])
def claim(id):
    return 'Claim %d' % id
