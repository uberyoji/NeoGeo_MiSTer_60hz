#!/usr/bin/python3

import sys
import os
import hashlib
import time
import json

# Add the following to /media/fat/downloader.ini
# [uberyoji_neogeo_mister_60hz]
# db_url = db_url = https://raw.githubusercontent.com/uberyoji/NeoGeo_MiSTer_60hz/master/releases/uberyoji_neogeo_mister_60hz.json

db_name = "uberyoji_neogeo_mister_60hz"
db_filename = db_name+".json"

db_url= "https://raw.githubusercontent.com/uberyoji/NeoGeo_MiSTer_60hz/master/releases/"

def get_file_props( entry ):
    pathname = entry[0]
    filename = entry[1]
    fullname = entry[1] # "../Games/{}".format(entry[1])

    if os.path.isfile(fullname):
        file_entry ="""
            "{0}": {{
                "hash": "{1}",
                "size": {2},
                "url": "{3}",
                "tags": [],
                "overwrite": true,
                "reboot": false
            }}"""
        return file_entry.format( pathname, hashlib.md5(open(fullname,'rb').read()).hexdigest(), os.path.getsize(fullname), "{}{}".format( db_url, filename ) )
    else:
        print( "{} not found".format(filename) )
        return ""

flist = [
    ("_Console/NeoGeo60hz_20260404.rbf","NeoGeo60hz_20260404.rbf")      # mister path+file, file
]

def validate(text):
    try:
        json.loads(text)
        print('valid json')
        return True
    except ValueError as e:
        print('invalid json: %s' % e)
        return False # or: raise

def build_json():
    json = """
    {{    

        "db_id": "{0}",
        "timestamp": {1},
        "base_files_url": "",
        "default_options": {{}},
        "folders": {{
            "_Console": {{}}    
        }},
        "files": {{
            {2}
        }}        
    }}
    """

    files = ""
    for r in flist:
        files += get_file_props(r)
        files += ",\n"
    
    files = files[:-2]  # trim last comma

    return json.format( db_name, int(time.time()), files )

json_content = build_json();
print( json_content )

if validate(json_content):
    json_file = open(db_filename,"w",encoding="utf8")
    json_file.write(json_content)
    json_file.flush()
    json_file.close()
    print('Done')
else:
    print('Something went wrong.')
