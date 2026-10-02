"""HAR capture check. Serve ./site on 127.0.0.1:8765 first:
   python3 -m http.server 8765 --bind 127.0.0.1 --directory site
Requires playwright==1.56.0 (pins Chromium build 1194). Verification only, not product code."""
import json, hashlib, base64
from playwright.sync_api import sync_playwright
served = open('site/jobs.json', 'rb').read()
with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(record_har_path='cap.har', record_har_content='embed', record_har_mode='full')
    pg = ctx.new_page(); pg.goto('http://127.0.0.1:8765/index.html'); pg.wait_for_selector('li[data-id="102"]')
    dom = pg.content(); ctx.close(); ver = b.version; b.close()
har = json.load(open('cap.har'))
e = [x for x in har['log']['entries'] if x['request']['url'].endswith('/jobs.json')][0]
c = e['response']['content']
body = base64.b64decode(c['text']) if c.get('encoding') == 'base64' else c['text'].encode()
print('chromium', ver)
print('XHR body byte-identical:', hashlib.sha256(body).digest() == hashlib.sha256(served).digest())
d = json.loads(body); print('len==unique==meta.total:', len(d['jobs']) == len({j['id'] for j in d['jobs']}) == d['meta']['total'])
print('rendered DOM has job 102:', 'data-id="102"' in dom)
