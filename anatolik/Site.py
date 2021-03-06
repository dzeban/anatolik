#!/usr/bin/env python3

import yaml
import os
import locale
import pickle
from collections import OrderedDict

class Site(object):
    config_path = "settings.yml"
    config  = {} # Parsed settings.yml
    info    = {} # General site info
    root    = {} # Map of filepath roots
    layouts = {} # Map of layout objects
    posts   = OrderedDict() # Map of post objects
    categories = set() # Set of categories

    cache_name = '.cache'

################################
# Global configuration to import
#
site = Site()
################################

def init():
    """ Initialize global site configuration from settings.yml """
    global site

    with open(site.config_path) as f:
        config = yaml.load(f)
        site.config = config

        site.root['config'] = os.path.dirname(f.name)

        # Save dir roots relative to config root
        root = site.root['config']
        for k,v in site.config['dirs'].items():
            site.root[k] = os.path.join(root, v)

        for k,v in site.config['info'].items():
            site.info[k] = v

    locale.setlocale(locale.LC_ALL, site.info['locale'])

    cache_path = os.path.join(site.root['output'], site.cache_name)
    if os.path.exists(cache_path):
        with open(cache_path, 'rb') as cache_file:
            site.posts = pickle.load(cache_file)
