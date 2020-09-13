#!/usr/bin/env python3
import json
import os
import glob
import traceback
import time

cache_dir = os.path.expanduser('~/.nvpy')
files = glob.glob(cache_dir + '/*.json')

now = time.time()
is_valid = True
for file in files:
    with open(file) as f:
        obj = json.load(f)
        try:
            # See https://simplenotepy.readthedocs.io/en/latest/api.html#simperium-api-note-object
            assert 'key' in obj and type(obj['key']) == str
            assert 'deleted' in obj and type(obj['deleted']) in [bool, int]
            assert 'modifydate' in obj and type(obj['modifydate']) in [float, int]
            assert 'createdate' in obj and type(obj['createdate']) in [float, int]
            assert 'version' in obj and type(obj['version']) == int
            assert 'systemtags' in obj and type(obj['systemtags']) == list
            assert 'tags' in obj and type(obj['tags']) == list
            assert 'content' in obj and type(obj['content']) == str

            # Optional field for nvpy.
            if 'savedate' in obj:
                assert type(obj['savedate'] in [float, int])
                assert float(obj['savedate']) <= now
            # Required field for nvpy.
            assert 'syncdate' in obj and type(obj['syncdate'] in [float, int])
        except:
            print('{}  Invalid'.format(file))
            print(obj)
            print(traceback.format_exc())
            print('')
            is_valid = False
        else:
            print('{}  OK'.format(file))

if is_valid:
    print('Done.  All notes are valid!')
else:
    print('Done.  Some notes are broken :-(')
    print('See above log for details.')
    exit(1)
