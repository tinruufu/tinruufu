# ティン・ルーフ

this is the code that powers [@tinruufu](https://twitter.com/tinruufu), which
happens to include a small but useful danbooru api client as well as a utility
for downloading all images from a danbooru search result

## requirements

you need python 2.7 running on a unix-y system like linux or bsd or mac osx or
something; anything that has a text file i can read at `/usr/share/dict/words`

there are also some python things you can install with `pip install [package]`
to make stuff work

completely necessary:

- `requests`, which we use to hit the danbooru api and download files

optional:

- `gevent`, for if you want to download files in parallel (it'll work fine
  without it, but it'll be slower)
- `tweepy`, for tweeting

## configuration

you can set twitter and danbooru credentials if you like; make a file called
`secrets.py` in this directory and make it look something like this:

```python
danbooru_login = 'username'
danbooru_key = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'

token_key = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
token_secret = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
app_key = 'AAAAAAAAAAAAAAAAAAAAAAAAA'
app_secret = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
```

without danbooru credentials associated with a gold account, you won't be able
to access images with censored tags

without twitter keys, you won't be able to tweet

## components (in order of how likely i think you are to be interested in them)

### `dl.py` (the bit that downloads files)

to download all images containing nekomimi and red hair, for example, you would
run `python dl.py nekomimi red_hair`

files are downloaded to a `downloads` directory in the current working
directory

### `nt.py` (the library and thing that tweets)

`nt.py` is where the business happens; it includes the utilities that the rest
of the stuff uses and will try to tweet when invoked as a script

all arguments are taken as tags to filter by, just like `dl.py`

### `post_later.py` (the thing that makes the timing interesting)

a delayed wrapper `nt.py` that takes the same arguments and does the same
thing, but waits a random interval between 0 and 48 hours before doing
anything.
