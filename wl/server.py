import flask
import mysql.connector
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
        cursor.execute("""
        SELECT item.*, (claim.item_id IS NOT NULL) as claimed FROM item
        LEFT JOIN claim ON item.id = claim.item_id
        WHERE item.id = %d
        """ % id)
        result = util.get_one(cursor)

        cursor.execute("""
        SELECT path, link
        FROM image
        WHERE item_id = %d
        """ % id)
        result['images'] = util.get_many(cursor)

        return result


# Pages

@app.route('/favicon.ico')
def favicon():
    return flask.redirect('/static/img/favicon.ico')


@app.route('/')
def page_list():
    return flask.render_template(
        'list.html',
        error=flask.request.args.get('error'))


@app.route('/detail/<int:id>')
def page_detail(id):
    return flask.render_template('detail.html', item=get_detail(id))


@app.route('/claiming/<int:id>')
def page_claiming(id):
    return flask.render_template('claiming.html', item=get_detail(id))


@app.route('/claim/<int:id>', methods=['POST'])
def page_claim(id):
    name = flask.request.form['name']
    email = flask.request.form['email']
    try:
        with get_cursor() as cursor:
            cursor.execute("""
            INSERT INTO claim
            (item_id, name, email, time, note)
            VALUES (%s, %s, %s, now(), "")
            """, (id, name, email))
            cursor._connection.commit()
    except mysql.connector.errors.IntegrityError:
        return flask.redirect('?error=already-claimed')
    return flask.redirect('/claimed?email=' + email)


@app.route('/unclaim/<email>/<int:id>', methods=['POST'])
def page_unclaim(email, id):
    with get_cursor() as cursor:
        cursor.execute("""
        DELETE FROM claim
        WHERE item_id = %s AND email = %s
        """, (id, email))
        cursor._connection.commit()
    return flask.redirect('/claimed?email=' + email + '&message=unclaimed')


@app.route('/claimed')
def page_claimed():
    if 'email' in flask.request.args:
        return flask.render_template('claimed_by.html',
                                     email=flask.request.args['email'],
                                     message=flask.request.args.get('message'))
    else:
        return flask.render_template('claimed.html')


# App

@app.route('/item/unclaimed')
def item_unclaimed():
    with get_cursor() as cursor:
        cursor.execute("""
        SELECT item.id, item.title
        FROM item
        LEFT JOIN claim ON item.id = claim.item_id
        WHERE claim.item_id IS NULL
        ORDER BY item.value
        """)
        return flask.jsonify(util.get_many(cursor))


@app.route('/item/claimed_by/<email>')
def item_claimed_by(email):
    with get_cursor() as cursor:
        cursor.execute("""
        SELECT item.id, item.title
        FROM item
        JOIN claim ON item.id = claim.item_id
        WHERE claim.email = %s
        """, (email,))
        return flask.jsonify(util.get_many(cursor))


@app.route('/item/<int:id>/detail')
def item_detail(id):
    return flask.jsonify(get_detail(id))
