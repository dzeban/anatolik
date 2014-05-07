#!/usr/bin/env python3

from .Config import site
from . import Util

class Layout(object):
    def __init__(self):
        self.name = ''
        self.data = ''
        self.html = ''

    def load(self, filepath):
        print('Loading layout {}'.format(filepath))

        with open(filepath) as f:
            self.content = f.read()
        
        self.name = Util.name( filepath ) 
        return True
