#!/usr/bin/env python3

import yaml
import os
import locale

class Site(object):
    config_path = "settings.yml"
    config  = {} # Parsed settings.yml
    root    = {} # Map of filepath roots
    layouts = {} # Map of layout objects
    posts   = {} # Map of post objects
    pages   = [] # List of page objects
    categories = set() # Set of categories

################################
# Global configuration to import
#
site = Site()
################################

def init():
    """ Initialize global site configuration from settings.yml """
    global site

    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

    with open(site.config_path) as f:
        config = yaml.load(f)
        site.config = config

        site.root['config'] = os.path.dirname(f.name)

        # Save dir roots relative to config root
        root = site.root['config']
        for k,v in site.config['dirs'].items():
            site.root[k] = os.path.join(root, v)
