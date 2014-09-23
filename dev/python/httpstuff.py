#!/usr/bin/env python

"""
Original author: Paul Boddie <paul@boddie.org.uk>

To the extent possible under law, the person who associated CC0 with this work
has waived all copyright and related or neighboring rights to this work.

See: http://creativecommons.org/publicdomain/zero/1.0/
"""

import sgmllib

class MyParser(sgmllib.SGMLParser):
    "A simple parser class."

    def parse(self, s):
        "Parse the given string 's'."
        self.feed(s)
        self.close()

    def __init__(self, verbose=0):
        "Initialise an object, passing 'verbose' to the superclass."

        sgmllib.SGMLParser.__init__(self, verbose)
        self.hyperlinks = []
        self.descriptions = []
        self.inside_a_element = 0
        self.starting_description = 0

    def start_a(self, attributes):
        "Process a hyperlink and its 'attributes'."

        for name, value in attributes:
            if name == "href":
                self.hyperlinks.append(value)
                self.inside_a_element = 1
                self.starting_description = 1

    def end_a(self):
        "Record the end of a hyperlink."

        self.inside_a_element = 0

    def handle_data(self, data):
        "Handle the textual 'data'."

        if self.inside_a_element:
            if self.starting_description:
                self.descriptions.append(data)
                self.starting_description = 0
            else:
                self.descriptions[-1] += data

    def get_hyperlinks(self):
        "Return the list of hyperlinks."

        return self.hyperlinks

    def get_descriptions(self):
        "Return a list of descriptions."

        return self.descriptions

import urllib, sgmllib

# Get something to work with.
f = urllib.urlopen("http://www.python.org")
s = f.read()

# Try and process the page.
# The class should have been defined first, remember.
myparser = MyParser()
myparser.parse(s)

# Get the hyperlinks.
print myparser.get_hyperlinks()
print myparser.get_descriptions()

import libxml2dom
doc = libxml2dom.parseString(s, html=1)
a_elements = doc.getElementsByTagName("a")
print 'now with libxml2dom'
for a in a_elements:
	print str(a)
