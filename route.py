from functools import lru_cache
import time
from flask import Blueprint, request, jsonify

from googleapiclient.discovery import build

# the google api_key and cse_id 
from const import *

from grab import Grab

bp = Blueprint('route', __name__, url_prefix='/api/umbra/')

@bp.route('/google')
def search_nonsense_content():
    keyword = request.args.get('keyword')
    page = int(request.args.get('page'))
    print('[INFO] google: ', keyword, page)

    start = (page - 1) * 10 + 1

    @lru_cache(maxsize=64)
    def google_search(search_term, api_key, cse_id, num, start):
        service = build("customsearch", "v1", developerKey=api_key)
        res = service.cse().list(q=search_term, cx=cse_id, num=num, start=start).execute()
        return res

    try:
        res = google_search(keyword, api_key, cse_id, num=10, start=start)
        if 'items' in res:
            return jsonify(res['items'])
        else:
            return jsonify({
                'success': False,
            })
    except Exception as e:
        print('[ERROR]', e)
        return jsonify({
            'success': False,
        })



@bp.route('/yhdm')
def search_yhdm():
    keyword = request.args.get('keyword')
    # crawl the urls...
    print('[INFO] yhdm', keyword)

    # TODO: proper response to for too many results (slow, and not necessary)
    def crawl(keyword):
        urls = []
        g = Grab()
        g.go(f'http://www.yhdm.so/search/{keyword}/')
        candidate_selectors = g.doc(f'//div[@class="lpic"]/ul/li/a/@href')
        # tmpfix: avoid too many inaccurate results
        if len(candidate_selectors) >= 3:
            candidate_selectors = candidate_selectors[[0]]
            print(f'[WARN] too many candidates for {keyword}, only keep the first.')
        # for candidates
        for candidate in candidate_selectors:
            g.go(f'http://www.yhdm.so{candidate.text()}')
            episode_selectors = g.doc('//div[@class="movurl"]/ul/li/a/@href')
            # tmpfix: avoid too many episodes
            if len(episode_selectors) >= 30:
                episode_selectors = episode_selectors[:12]
                print(f'[WARN] too many episodes, only keep the first 12.')
            # for episodes
            for episode in episode_selectors:
                g.go(f'http://www.yhdm.so{episode.text()}')
                title_selectors = g.doc('//div[@class="gohome l"]/h1')
                data_selectors = g.doc('//div[@id="playbox"]/@data-vid')
                title = title_selectors[0].text()
                url = data_selectors[0].text()
                # tmpfix 
                if url[-4:] == "$mp4":
                    url = url[:-4]
                # append to results
                print(f'[INFO] crawled {title} {url}')
                urls.append({
                    'formattedUrl': url,
                    'title': title,
                    'snipped': '',
                })
        return urls
        
    try:
        urls = crawl(keyword)
        res = {}
        res['success'] = True
        res['results'] = urls
        return jsonify(res)
    except Exception as e:
        return jsonify({
            'success': False,
        })
        