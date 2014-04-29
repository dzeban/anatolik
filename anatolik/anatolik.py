#!/usr/bin/env python3

import sys
import os
import shutil
from glob import glob
from pprint import pprint
from collections import OrderedDict

from .Config import site
from .Config import init as site_init

from .Layout import Layout
from .Post import Post

from .Util import copy_dir

__version__ = "0.1"

def parse_files():
    print('\n [:::  Files processing :::]\n')

    path = site.root['content']
    print('Looking for files in {}'.format(path))

    # Collect posts files
    files_list = []
    site.md_files = []
    for root, dirs, files in os.walk( path ):
        if( len(files) == 0): # Don't care about empty dirs
            continue
        
        for f in files:
            files_list.append(root + os.sep + f)

        site.md_files.extend(glob(root + os.sep + '*.md'))

    site.files = [item for item in files_list if item not in site.md_files] 

def parse_posts():
    print('\n [:::  Posts processing :::]\n')

    # Load post files into objects
    for path in site.md_files:
        p = Post()
        if p.load(path) is True:
            site.posts[ p.Slug ] = p

    site.posts = OrderedDict(sorted(site.posts.items(), key = lambda p: p[1].Date, reverse = True))
    
def parse_layouts():
    print('\n [:::  Layouts processing :::]\n')

    layouts_path = site.root['layouts']
    print('Looking for layouts in {}'.format(layouts_path))

    # Collect layout files
    layouts = []
    for root, dirs, files in os.walk( layouts_path ):
        if( len(files) == 0): # Don't care about empty dirs
            continue
        layouts.extend(glob(root + os.sep + '*.tmpl'))
    
    for path in layouts:
        l = Layout()
        l.load(path)
        site.layouts[l.name] = l

def render():
    print('\n [:::  Rendering :::]\n')
    for post in site.posts.values():
        post.render()
        post.render_layout()

def create_output():
    print('\n [:::  Writing output :::]\n')
    out_dir = site.root['output']
    for post in site.posts.values():
        path = os.path.join(out_dir, post.Url)
        os.makedirs(os.path.dirname(path), exist_ok = True)
        with open(path, 'w') as f:
            f.write(post.content)
        print(path)

    for f in site.files:
        file_path = f.split(site.root['content'])[-1]
        file_path = file_path[1:] # Cut first '/'
        path = os.path.join(out_dir, file_path)
        print(path)
        os.makedirs(os.path.dirname(path), exist_ok = True)
        if os.path.exists(path):
            os.remove(path)
        shutil.copy(f, path)

def usage():
    print("main.py [config path]")

def main():
    # Get path to config
    if len(sys.argv) == 2:
        site.config_path = sys.argv[1]
    else:
        usage()
        sys.exit(1)

    site_init()
    print('Parsed config:');  pprint(site.config); print('---')

    parse_files()
    parse_posts()
    parse_layouts()
    render()
    create_output()

#if __name__ == "__main__":
#    main()
