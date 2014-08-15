#!/usr/bin/env python

from .Site import site

import flickrapi
import re
import sys
import pdb

from urllib.parse import urlparse

class Flickr:

    static_link_template = "http://farm%s.staticflickr.com/%s/%s_%s_c.jpg"
    regex    = 'flickr://[A-Za-z_/0-9]+'
    user_id  = ''
    config   = ''
    api_key  = ''
    api_pass = ''

    def __init__(self):
        config   = site.config['flickr']
        self.user_id  = config['user_id']
        self.api_key  = config['api_key']
        self.api_pass = config['api_password']
    
        self.flickr = flickrapi.FlickrAPI(self.api_key, self.api_pass, self.user_id)

    def find_set (self, pset, ptitle):
        set_id = False
        for s in pset.iter():
            if s.tag == 'photoset':
                for st in s.getchildren():
                    if st.text == ptitle:
                        found_set = s

        if len(found_set.attrib) != 0:
            set_id = found_set.attrib['id']
        return set_id

    def form_url (self, pattr):
        pu = self.static_link_template % (pattr['farm'], pattr['server'], pattr['id'], pattr['secret'])
        return pu

    def get_url(self, set_ph, photo_t):
        ph_url = ''
        for ph in set_ph.iter():
            if ph.tag == 'photo':
                photo_title = ph.attrib['title'].split('.')[0]
                if photo_title == photo_t:
                    pa = ph.attrib
                    ph_url = self.form_url(pa)
        return ph_url

    def static_url( self, album, photo ):
        sets = self.flickr.photosets_getList(user_id = self.user_id)
        set_id = self.find_set(sets, album)
        set_photos = self.flickr.photosets_getPhotos(api_key = self.api_key, photoset_id = set_id)
        return self.get_url(set_photos, photo)

    def parse_url(self, url):
        parsed = urlparse(url)
        album = parsed.netloc
        photo = parsed.path.strip('/')
        return album, photo

    def parse_urls(self, text):
        for flickurl in re.finditer(self.regex, text):
            album, photo = self.parse_url(flickurl.group(0))
            static_url = self.static_url( album, photo)
            text = text.replace(flickurl.group(0), static_url)
        return text

