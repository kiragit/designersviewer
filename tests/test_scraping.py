# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 13:32:01 2015

@author: kentarokira
"""

import pytest
from app.scraping import * 
import lxml.html
import lxml.cssselect

def test_sample():
    HTML="""
    <html>
      <head></head>
      <body></body>
        <div class='pure-menu-heading'>
          <p>2014.04.14</p>
        </div>
    </html>
    """
    p="cssselect"
    c=".pure-menu-heading"
    s=".all"
    h=""
    
    HTML_element = lxml.html.fromstring(HTML)
    assert htmlItemSelector(HTML_element,p,c,s,h)=="2014.04.14"
