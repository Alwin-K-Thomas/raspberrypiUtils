#!/usr/bin/python

import ConfigParser
import os
import pprint


class parseSecretsHere(object):
    def __init__(self, secretFile):
        self.file = secretFile
        self.configuration = {}

    def parseFileSections(self):
        self.config = ConfigParser.ConfigParser()
        if os.path.exists(self.file):
            self.config.read(self.file)

    def parseFileOptions(self):
        self.parseFileSections()
        for section in self.config.sections():
            self.configuration[section] = {}
            for option in self.config.options(section):
                self.configuration[section][option] = self.config.get(section, option)

    def printThemPretty(self):
        return pprint.pformat(self.configuration)

if __name__ == "__main__":
    p = parseSecretsHere('secrets.ini')
    p.parseFileOptions()
    print p.printThemPretty()
        
