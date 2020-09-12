import time
from flask import Blueprint, request, jsonify

from googleapiclient.discovery import build
from const import *

bp = Blueprint('route', __name__, url_prefix='/api/umbra/')

#@bp.route('/')
#def hello():
#    return "Hello!"

# =========== Nonsense ===========
# currently, we leave exception handling with frontend. 


@bp.route('/search')
def search_nonsense_content():
    keyword = request.args.get('keyword')
    page = int(request.args.get('page'))
    print(keyword, page)

    start = (page - 1) * 10 + 1

    def google_search(search_term, api_key, cse_id, **kwargs):
        service = build("customsearch", "v1", developerKey=api_key)
        res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
        return res

    res = google_search(keyword, api_key, cse_id, num=10, start=start)

    if 'items' in res:
        return jsonify(res['items'])
    else:
        return jsonify({})
