#!/usr/bin/python
# Released under The Unlicense <http://unlicense.org/>
# Written by Taj Morton <tajmorton@gmail.com>
# See the accompying UNLICENSE file for more information.

import sys
import urllib2
from HTMLParser import HTMLParser

class CountryParser(HTMLParser):
    AWAITING_COUNTRY_LIST, IN_COUNTRY_LIST, READING_ENTRY, DONE = (0, 1, 2, 3)
    def __init__(self):
        HTMLParser.__init__(self)

        self.current_state = self.AWAITING_COUNTRY_LIST
        self.country_list = []

    def handle_starttag(self, tag, attrs):
        if tag == "select":
            for key, val in attrs:
                if key == "name" and val.endswith("$DropDownListCountry"):
                    self.current_state = self.IN_COUNTRY_LIST
                    break
        elif self.current_state == self.IN_COUNTRY_LIST and tag == "option":
            self.current_state = self.READING_ENTRY
            

    def handle_endtag(self, tag):
        if tag == "select" and self.current_state == self.IN_COUNTRY_LIST: 
            self.current_state = self.DONE
        elif tag == "option" and self.current_state == self.READING_ENTRY:
            self.current_state = self.IN_COUNTRY_LIST

    def handle_data(self, data):
        if self.current_state == self.READING_ENTRY:
            if data.strip() not in self.country_list: # list contains some duplicates
                self.country_list.append(data.strip())

if __name__ == "__main__":
    if len(sys.argv) > 1:
        country_file = open(sys.argv[1], 'r')
    else:
        country_file = urllib2.urlopen("http://ircalc.usps.gov/")

    parser = CountryParser()
    parser.feed(country_file.read())

    parser.close()
    country_file.close()

    for country in parser.country_list:
        print country

