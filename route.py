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
    token = request.args.get('token')
    db = mysql.get_db()
    cur = db.cursor()
    cur.execute(stmt_meta, (token,))
    meta = cur.fetchall()
    cur.close()
    db.close()
    return jsonify(meta)

@bp.route('/post')
def post_nonsense():
    token = request.args.get('token')
    ctime = time.time()
    mtime = ctime
    body = '' # empty when created
    db = mysql.get_db()
    cur = db.cursor()
    cur.execute(stmt_post, (ctime, mtime, body, token))
    db.commit()
    # get nid
    cur.execute(stmt_size)
    nid = cur.fetchone()[0]
    cur.close()
    db.close()
    return jsonify({
        'success': True,
        'nid': nid,
        'ctime': ctime,
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
        })

@bp.route('/search')
def search_nonsense_content():
    token = request.args.get('token')
    keyword = request.args.get('keyword')
    db = mysql.get_db()
    cur = db.cursor()
    cur.execute(stmt_search, (keyword, token))
    res = cur.fetchall()
    cur.close()
    db.close()
    return jsonify(res)

@bp.route('/delete', methods=('POST', ))
def delete_nonsense_content():
    nid = request.form['nid']
    db = mysql.get_db()
    cur = db.cursor()
    cur.execute(stmt_delete, (nid,))
    db.commit()
    cur.close()
    db.close()
    return jsonify({
        'success': True,
        })