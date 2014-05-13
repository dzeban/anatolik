#!/usr/bin/env python3

import os
import yaml
from datetime import date
from pwd import getpwuid
from zlib import crc32

from markdown import markdown
from pypandoc import convert
from mako.template import Template
from mako.lookup import TemplateLookup


from .Config import site
from .flickr import Flickr
from . import Util


class Post(object):
    def __init__(self):
        self.Title = ''
        self.Author =''
        self.Date = ''
        self.Category = ''
        self.Slug = ''
        self.Layout = ''
        self.Draft = False
        self.Mako = False
        self.Flickr = False

        self.front_matter = ''
        self.markup = ''
        self.html = ''
        self.content = ''

        self.crc32 = 0

    def __str__(self):
        return '{}: [{}] in {}, {}'.format(self.Slug, self.Date, self.Category, self.Layout)

    def parse_front_matter(self, front_matter):
        if len(front_matter) is 0: # Nothing to do here
            return True 

        fm = yaml.load(front_matter)
        for key in fm:
            setattr(self, key, fm[key])
        
        return True

    def parse_file_attrs(self, f):
        """ Fill object attributes from file attributes """
        stat = os.stat(f.name)

        self.Slug = Util.name(f.name) # slug from filename
        self.Title = self.Slug
        self.Date = date.fromtimestamp(stat.st_ctime) # date from file ctime
        self.Author = getpwuid(stat.st_uid).pw_name # author from uid

        # Set category from file parent directory
        path = f.name.replace(site.root['content'] + os.sep, '')
        self.Category = os.path.split(path)[0]
        site.categories.add( self.Category )

        # Set layout from settings or empty if not set
        # (.get() is used to not get KeyError)
        self.Layout = site.config['post'].get('default_layout','')

    def load(self, filepath):

        with open(filepath) as f:
            data = f.read()
            self.parse_file_attrs(f)

        try:
            front_matter, self.markup = data.split('---', 1)
            self.parse_front_matter(front_matter) 
        except: # ValueError, yaml.ScannerError
            print('> Invalid front matter format in {}'.format(filepath))
            return False

        if( self.Draft is True ):
            print('> Skipping draft {}'.format(filepath))
            return False

        self.Url = os.path.join(self.Category, self.Slug) + '.html'

        self.crc32 = crc32(bytes(self.markup, 'utf8'))

        return True

    def render(self):
        # Render templates if explicitly set
        if self.Mako is True:
            template = Template(self.markup)
            self.markup = template.render(site = site, current = self)

        if self.Flickr is True:
            flickr = Flickr()
            self.markup = flickr.parse_urls(self.markup)

        # Render markdown
        self.html = convert(source=self.markup, to='html', format='markdown', 
                                extra_args=site.config['markdown']['extra_args'])

    def render_layout(self):
        # Lookup post template
        layout = site.layouts[ self.Layout ]

        print('Rendering post {} in layout {}'.format(self.Slug, layout.name))

        lookup = TemplateLookup(directories=[site.root['layouts']]) # Lookup is needed for <%include/>
        template = Template( layout.content, lookup = lookup )
        self.content = template.render(site = site, post = self)
