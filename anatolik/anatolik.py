#!/usr/bin/env python3

import sys
import os
import shutil
from glob import glob
from pprint import pprint
from collections import OrderedDict
import pdb

from .Config import site
from .Config import init as site_init

from .Layout import Layout
from .Post import Post

from .Util import copy_dir

__version__ = "0.1"

def parse():
    path = site.root['config']
    all_files = set()
    posts = set()
    layouts = set()

    for root, _, files in os.walk(path):
        if (len(files) == 0): # Don't care about empty dirs
            continue

        for f in files:
            all_files.add(root + os.sep + f)
        posts |= set(glob(root + os.sep + site.config['posts']))
        layouts |= set(glob(root + os.sep + site.config['layouts']))

    site.files = all_files - posts - layouts
    site.post_files = posts
    site.layout_files = layouts

def load():
    for path in site.post_files:
        p = Post()
        if p.load(path):
            site.posts[p.Slug] = p
    
    for path in site.layout_files:
        l = Layout()
        if l.load(path):
            site.layouts[l.name] = l

    site.posts = OrderedDict(sorted(site.posts.items(), key = lambda p: p[1].Date, reverse = True))

def render():
    print('\n [:::  Rendering :::]\n')
    for post in site.posts.values():
        post.render()
        post.render_layout()

def output():
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
    parse()
    load()
    render()
    output()
