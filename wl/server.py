import flask
from . import util
app = flask.Flask(__name__)


def get_db():
    if not hasattr(flask.g, 'db_conn'):
        flask.g.db_conn = util.connect()
    return flask.g.db_conn


def get_cursor():
    return util.UsingCursor(get_db())


@app.teardown_appcontext
def close_db(error):
    if hasattr(flask.g, 'db_conn'):
        flask.g.db_conn.close()


def get_detail(id):
    with get_cursor() as cursor:
        cursor.execute('SELECT * FROM item WHERE id = %d' % id)
        result = util.get_one(cursor)

        cursor.execute('''
        SELECT path, link
        FROM image
        WHERE item_id = %d
        ORDER BY thumb DESC
        ''' % id)
        result['images'] = util.get_many(cursor)

        return result


# Pages

@app.route('/')
def page_list():
    return flask.render_template('list.html')


@app.route('/detail/<int:id>')
def page_detail(id):
    return flask.render_template('detail.html', item=get_detail(id))


# App

@app.route('/item')
def item():
    with get_cursor() as cursor:
        cursor.execute('''
        SELECT item.id, item.title, image.path
        FROM item
        LEFT JOIN image ON item.id = image.item_id
        WHERE image.thumb = 1
        ''')
        return flask.jsonify(util.get_many(cursor))


@app.route('/item/<int:id>/detail')
def item_detail(id):
    return flask.jsonify(get_detail(id))


@app.route('/item/<int:id>/claim', methods=['POST'])
def item_claim(id):
    # TODO
    return 'Claim %d' % id
