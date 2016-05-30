#!/usr/bin/env python

import os
import sys
import urllib
import webbrowser

import pickledb
import requests

BASE_URL = 'https://unsplash.com'
BASE_API_URL = 'https://api.unsplash.com'
CLIENT_ID = ''
CLIENT_SECRET = ''

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, 'images')

query = 'landscape'
swift_app_path = os.path.join(BASE_DIR, 'app.swift')
db = pickledb.load(os.path.join(BASE_DIR, 'data.db'), False)


def check_images_dir():
    if not os.path.isdir(IMAGES_DIR):
        os.makedirs(IMAGES_DIR)


def authorize():
    url = BASE_URL + '/oauth/authorize'
    params = {
        'client_id': CLIENT_ID,
        'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob',
        'response_type': 'code',
        'scope': 'public'
    }
    webbrowser.open('{}?{}'.format(url, urllib.urlencode(params)), new=2)


def request_token(authorization_code):
    url = BASE_URL + '/oauth/token/'
    response = requests.post(url, data={
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob',
        'code': authorization_code,
        'grant_type': 'authorization_code'
    })
    return response.json()


def refresh_access_token(refresh_token):
    url = BASE_URL + '/oauth/token/'
    response = requests.post(url, data={
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'refresh_token': refresh_token,
        'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob',
        'grant_type': 'refresh_token'
    })
    return response.json()


def request_random_photo(access_token):
    response = requests.get(BASE_API_URL + '/photos/random?query=' + query, headers={
        'Authorization': 'Bearer {}'.format(access_token)
    })
    if response.status_code == 200:
        data = response.json()
        id_ = data['id']
        image_url = data['urls']['full']
        image_path = os.path.join(IMAGES_DIR, '{}.jpg'.format(id_))
        urllib.urlretrieve(image_url, image_path)
        os.popen('/usr/bin/swift {} {}'.format(swift_app_path, image_path))
        return True
    return False


def main():
    try:
        access_token = db.get('access_token')
        refresh_token = db.get('refresh_token')
        if not request_random_photo(access_token):
            data = refresh_access_token(refresh_token)
            access_token = data['access_token']
            refresh_token = data['refresh_token']
            request_random_photo(access_token)
            db.set('access_token', access_token)
            db.set('refresh_token', refresh_token)
            db.dump()
    except KeyError:
        print('Please run python app.py authorize')
    

if __name__ == '__main__':
    check_images_dir()
    if len(sys.argv) == 2:
        command = sys.argv[1]
        if command.lower() == 'authorize':
            authorize()
            code = raw_input('Please enter authorization code: ')
            data = request_token(code)
            db.set('access_token', data['access_token'])
            db.set('refresh_token', data['refresh_token'])
            db.dump()
            print('authorization successful :)')
    main()
