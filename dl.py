import os
from sys import argv

try:
    from gevent import joinall, monkey, spawn
except ImportError:
    print 'gevent is not installed, downloads will be single-threaded'
    joinall = lambda *a, **k: None
    spawn = lambda f, *a, **k: f(*a, **k)
else:
    monkey.patch_all()

from nt import get_page, download, HERE, URL


TARGET_DIR = os.path.join(HERE, 'downloads')


def dl(url, target):
    filename = download(url)
    os.rename(filename, target)
    print 'download complete: %s' % url


def get_posts(tags):
    pageno = 1

    if not os.path.isdir(TARGET_DIR):
        os.mkdir(TARGET_DIR)

    while True:
        print pageno
        page = get_page(tags, pageno)

        if len(page) == 0:
            break

        tasks = []

        for post in page:
            if 'file_url' not in post:
                print 'post %s has no url; skipping' % post['id']
                continue

            url = URL.format(post['file_url'])
            basename = url.split('/')[-1]
            target = os.path.join(TARGET_DIR, basename)

            if os.path.exists(target):
                if os.path.getsize(target) > 0:
                    print '%s :: skipping; already present' % post['file_url']
                    continue
                else:
                    print '%s :: file empty, downloading' % post['file_url']

            tasks.append(spawn(dl, url, target))

        print 'downloading %i files' % len(tasks)

        joinall(tasks, raise_error=True)

        pageno += 1


if __name__ == '__main__':
    get_posts(argv[1:])
