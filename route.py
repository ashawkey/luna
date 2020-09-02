import time
from flask import Blueprint, request, jsonify
from mysql import *

bp = Blueprint('route', __name__, url_prefix='/api/nonsense/')

#@bp.route('/')
#def hello():
#    return "Hello!"

# =========== Nonsense ===========

@bp.route('/meta')
def get_nonsense_meta():
    db = mysql.get_db()
    cur = db.cursor()
    cur.execute(stmt_meta)
    meta = cur.fetchall()
    cur.close()
    db.close()
    return jsonify(meta)

@bp.route('/post', methods=('POST',))
def post_nonsense():
    ctime = time.time()
    mtime = ctime
    body = '' # empty when created
    db = mysql.get_db()
    cur = db.cursor()
    cur.execute(stmt_post, (ctime, mtime, body))
    db.commit()
    # get nid
    cur.execute(stmt_size)
    nid = cur.fetchone()[0]
    cur.close()
    db.close()
    return jsonify({
        'success': True,
        'status_code': 200,
        'nid': nid,
        })

@bp.route('/get')
def get_nonsense_content():
    nid = request.args.get('nid')
    db = mysql.get_db()
    cur = db.cursor()
    cur.execute(stmt_get, (nid,))
    content = cur.fetchone()
    cur.close()
    db.close()
    if content is None:
        return jsonify({
            'success': False,
        })
    else:
        return jsonify({
            'success': True,
            'content': content,
        })

@bp.route('/update', methods=('POST', ))
def update_nonsense_content():
    mtime = time.time()
    nid = request.form['nid']
    body = request.form['body']
    db = mysql.get_db()
    cur = db.cursor()
    cur.execute(stmt_update, (mtime, body, nid))
    db.commit()
    cur.close()
    db.close()
    return jsonify({
        'success': True,
        "status_code": 200,
        })

@bp.route('/search')
def search_nonsense_content():
    keyword = request.args.get('keyword')
    db = mysql.get_db()
    cur = db.cursor()
    cur.execute(stmt_search, (keyword,))
    res = cur.fetchall()
    cur.close()
    db.close()
    return jsonify(res)

@bp.route('/delete')
def delete_nonsense_content():
    nid = request.args.get('nid')
    db = mysql.get_db()
    cur = db.cursor()
    cur.execute(stmt_delete, (nid,))
    db.commit()
    cur.close()
    db.close()
    return jsonify({
        'success': True,
        "status_code": 200,
        })