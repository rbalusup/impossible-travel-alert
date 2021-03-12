#!/usr/bin/env python3

import os.path
from hashlib import md5
from time import time

import requests
import sqlite3
from yaml import safe_load


def load_config():
    configs = {}
    with open(".configs.yaml") as file:
        properties = safe_load(file)
        for key, value in properties.items():
            configs[key] = value
    return configs


def get_marvel_auth_params():
    auth_params = {}

    epoch_timestamp = int(time())
    timestamp_plaintext = str(epoch_timestamp) + api_private_key + api_public_key
    md5_hash = md5(timestamp_plaintext.encode("utf-8")).hexdigest()
    auth_params['ts'] = str(epoch_timestamp)
    auth_params['apikey'] = api_public_key
    auth_params['hash'] = md5_hash
    auth_params['limit'] = 100

    return auth_params


def database_setup(database_name):
    connect, cursor = db_connect(database_name)
    # Create tables
    cursor.execute('''CREATE TABLE comic_characters(id text, name text, description text, url text)''')
    cursor.execute('''CREATE TABLE similar_comic_characters(id text, name text, description text, url text)''')
    db_disconnect(connect)


def db_disconnect(connect):
    connect.commit()
    connect.close()


def db_connect(database_name):
    connect = sqlite3.connect(database_name)
    cursor = connect.cursor()
    return connect, cursor


def build_character_dict(item):
    character_dict = {'id': item['id'], 'name': item['name'], 'description': item['description']}

    image_path = item['thumbnail']['path']
    extension = item['thumbnail']['extension']
    character_dict['picture'] = image_path + '/' + image_size + '.' + extension

    return character_dict


def add_character_if_not_exists(character_dict):
    connect, cursor = db_connect(dbname)

    cursor.execute("SELECT * FROM comic_characters WHERE name=?", (character_dict['name'],))
    if cursor.fetchone() is None:
        print("Inserting " + character_dict['name'] + "to comic_characters table")

        formatted_parameters = (
            character_dict['id'], character_dict['name'], character_dict['description'], character_dict['picture'])

        sql = ''' INSERT INTO comic_characters(id, name, description, url) VALUES(?,?,?,?) '''

        # Insert data row
        cursor.execute(sql, formatted_parameters)
        db_disconnect(connect)


def obtain_character_information(character_info):
    connect, cursor = db_connect(dbname)

    cursor.execute("SELECT * FROM comic_characters WHERE name=?", (character_info,))
    character_record = cursor.fetchone()

    if character_record is None:
        url = (marvel_host_uri + 'characters')
        responses = requests.get(url, params=params).json()

        total = responses['data']['total']
        offset = responses['data']['offset']

        while offset < total:
            updated_responses = requests.get(url, params=params).json()
            offset = updated_responses['data']['offset']
            count = updated_responses['data']['count']

            for response in updated_responses['data']['results']:
                character_dict = build_character_dict(response)
                add_character_if_not_exists(character_dict)

                if character_info == response['name']:
                    char_id = response['id']
                    return char_id

            # pagination counters
            new_offset = (offset + count)
            params['offset'] = int(new_offset)
    else:
        # print('Character %s found with id %s' % (character_info, character_record[0]))
        char_id = character_record[0]
        return char_id


def save_similar_comic_characters(character_dict):
    connect, cursor = db_connect(dbname)

    cursor.execute("SELECT * FROM similar_comic_characters WHERE name=?", (character_dict['name'],))
    if cursor.fetchone() is None:
        print("Inserting " + character_dict['name'] + " to similar_comic_characters table")

        formatted_parameters = (character_dict['id'], character_dict['name'], character_dict['description'],
                                character_dict['picture'])

        sql = ''' INSERT INTO similar_comic_characters(id, name, description, url) VALUES(?,?,?,?) '''

        # Insert data row
        cursor.execute(sql, formatted_parameters)
        db_disconnect(connect)


def get_character_dict(item_id):
    endpoint = (marvel_host_uri + 'characters/' + str(item_id))
    response = requests.get(endpoint, params=params).json()
    character_dict = build_character_dict(response['data']['results'][0])
    return character_dict


def obtain_save_other_characters_info_from_other_comics(char_id):
    endpoint = (marvel_host_uri + 'characters/' + str(char_id) + '/comics')
    responses = requests.get(endpoint, params=params).json()
    for collection in responses['data']['results']:
        for item in collection['characters']['items']:
            item_id = obtain_character_information(item['name'])
            character_dict = get_character_dict(item_id)
            save_similar_comic_characters(character_dict)


config = load_config()
dbname = config['database']['name']
character_name = config['character']['name']
image_size = config['character']['image_size']
api_public_key = config['marvel']['public_key']
api_private_key = config['marvel']['private_key']
marvel_host_uri = config['marvel']['host']
params = get_marvel_auth_params()

if os.path.isfile(dbname):
    print("database already exists")
else:
    database_setup(dbname)

character_id = obtain_character_information(character_name)
obtain_save_other_characters_info_from_other_comics(character_id)
