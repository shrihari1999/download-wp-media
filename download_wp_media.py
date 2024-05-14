import os, requests, argparse
from pathlib import Path
from requests_futures.sessions import FuturesSession
from concurrent.futures import as_completed
from urllib.parse import urlparse
from urllib.parse import parse_qs

parser=argparse.ArgumentParser()
parser.add_argument("domain", help='wordpress domain')
parser.add_argument("--per_page", help='number of media elements per page', default=100)
args=parser.parse_args()

domain = args.domain
per_page = args.per_page
url = f"https://{domain}/wp-json/wp/v2/media"
response = requests.get(f"{url}?per_page={per_page}")
max_page = int(response.headers['X-WP-TotalPages'])

BASE_DIR = Path(__file__).resolve(strict=True).parent
DOWNLOAD_DIR = os.path.join(BASE_DIR, os.path.join('downloads', domain))

page_session = FuturesSession()
page_futures = []
for page in range(1, max_page+1):
    print(f"Loading page {page}...")
    page_future = page_session.get(f"{url}?per_page={per_page}&page={page}")
    page_futures.append(page_future)
print('All pages loaded.')

media_session = FuturesSession()
media_futures = []
for page_future in as_completed(page_futures):
    response = page_future.result()
    url = response.request.url

    if response.status_code == 400:
        print(f"Failed for {url}")
        continue
    
    response = response.json()
    parsed_url = urlparse(url)
    page = parse_qs(parsed_url.query)['page'][0]
    print(f"Scanning page {page}...")

    for media in response:
        media_future = media_session.get(media['source_url'])
        media_future.custom_data = {'post': media['post'], 'id': media['id']}
        media_futures.append(media_future)
print('All pages scanned.')

print('Downloading all collected posts...')
for media_future in as_completed(media_futures):
    response = media_future.result()
    source_url = response.request.url
    custom_data = media_future.custom_data

    file_extension = source_url.rsplit('.', 1)[1]
    path = os.path.join(os.path.join(DOWNLOAD_DIR, str(custom_data['post'])), f"{custom_data['id']}.{file_extension}")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        f.write(response.content)

print('Done')
