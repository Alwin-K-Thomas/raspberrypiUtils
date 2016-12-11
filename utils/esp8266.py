#!/usr/bin/python

import urllib2
from parseIni import parseSecretsHere
import getIpAddr
import os

baseDirectory = os.path.join(os.path.abspath(__file__), '../config/secrets.ini')

class ESP8266(object):
    """
    Contains the ReST calls for ESP8266
    """
    @staticmethod
    def pinMode(ipAddr ,mode, pin):
        """
        Set the pin mode.
        mode: mode str
        """
        p = parseSecretsHere(baseDirectory)
        configurations = p.parseFileOptions()
        print "xxxxxxxx",configurations
        ipAddrList = getIpAddr.getIpAddr.main()
        return "http://{0}/gpio?cmd=conf&gpio={1}&mode={2}".format(ipAddr, mode, pin)

    @staticmethod
    def pinOut(mode='in', pin=None):
        """
        Get the mode for ReST calls.
        mode: type str
        """
        requestUrl = ESP8266.setPinMode("192.168.5.12", mode, pin)
        esp8266Response = urllib2.urlopen(requestUrl)
        return esp8266Response


if __name__ == "__main__":
    print ESP8266.pinMode("192.168.5.12", "in", 2) 
    #ESP8266.getPinOut(mode="in", pin=2)
