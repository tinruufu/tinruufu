# coding=utf-8

from random import choice
import re
import os.path
from sys import argv
from urlparse import urljoin

import requests

try:
    from secrets import danbooru_login, danbooru_key
except ImportError:
    print (
        'no danbooru credentials provided, some posts will not have image '
        'urls so we will not be able to download them\n'
        'see README.md for more information'
    )
    danbooru_key = None
    danbooru_login = None


URL = 'https://danbooru.donmai.us{0}'
LIMIT = 100

HERE = os.path.dirname(__file__)

WORDS = []
SLURS = requests.get(
    'https://raw.githubusercontent.com/dariusk/wordfilter/'
    'master/lib/badwords.json'
).json()


def download(url):
    print(url)
    filename = os.path.join(HERE, url.split('/')[-1])
    content = requests.get(url).content

    with open(filename, 'w') as target:
        target.write(content)

    return filename


def danbooru(url, **params):
    if danbooru_key and danbooru_login:
        params.update({
            'login': danbooru_login,
            'api_key': danbooru_key,
        })

    resp = requests.get(
        URL.format(url), params=params,
    ).json()

    if not isinstance(resp, list):
        raise RuntimeError(resp)

    return resp


def get_page(tags, page):
    return danbooru('/posts.json', page=page, tags=' '.join(tags), limit=LIMIT)


def get_post_count(tags):
    """
    work out how many posts there are for a given collection of tags
    """

    page = 1

    while True:
        resp = get_page(tags, page)

        if len(resp) == 0:
            earliest_empty_page = page
            break
        else:
            latest_populated_page = page

        page *= 2

    while (earliest_empty_page - latest_populated_page) > 1:
        page = int((latest_populated_page + earliest_empty_page) / 2)
        resp = get_page(tags, page)

        if len(resp) == 0:
            earliest_empty_page = page
        else:
            latest_populated_page = page

    return (
        (latest_populated_page - 1) * LIMIT +
        len(get_page(tags, latest_populated_page))
    )


def get_random_image(tags):
    post_count = get_post_count(tags)
    post_number = choice(xrange(post_count))

    index_on_page = post_number % LIMIT
    page = ((post_number - index_on_page) / LIMIT) + 1
    post = get_page(tags, page)[index_on_page]

    filename = download(urljoin(URL.format(''), post['file_url']))
    pixiv_id = post.get('pixiv_id', None)
    source = None

    if pixiv_id:
        source = (
            'http://www.pixiv.net/member_illust.php?mode=medium&illust_id={}'
            .format(pixiv_id)
        )
    elif post.get('source'):
        try:
            resp = requests.get(post['source'])
        except requests.RequestException:
            pass
        else:
            if resp.status_code == 200:
                source = post['source']

    return (filename, source)


def is_bad(word):
    for slur in SLURS:
        if slur in word:
            return True

    return False


def populate_words():
    with open('/usr/share/dict/words') as wordlist:
        for line in wordlist.readlines():
            word = line.strip()

            if re.match(r'\w+$', word) and not is_bad(word):
                WORDS.append(word)


def random_word():
    if not WORDS:
        populate_words()

    return choice(WORDS)


def make_twitter_api():
    import tweepy
    from secrets import app_key, app_secret, token_key, token_secret

    auth = tweepy.OAuthHandler(app_key, app_secret)
    auth.set_access_token(token_key, token_secret)
    return tweepy.API(auth)


def post_random_image(tags):
    kwargs = {}

    words = []
    number_of_hashtags = choice(xrange(1, 4))
    for i in xrange(number_of_hashtags):
        words.append('#{word}'.format(word=random_word()))

    filename, source = get_random_image(tags)

    if source:
        words.append(source)

    kwargs['status'] = ' '.join(words)

    make_twitter_api().update_with_media(filename, **kwargs)


if __name__ == '__main__':
    post_random_image(argv[1:])
