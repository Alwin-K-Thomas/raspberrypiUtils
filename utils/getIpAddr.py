#!/usr/bin/python

from __future__ import absolute_import, division, print_function
import logging
import scapy.config
import scapy.layers.l2
import scapy.route
import socket
import math
import errno
import pprint

logging.basicConfig(format='%(asctime)s %(levelname)-5s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)
logger = logging.getLogger(__name__)

class getIpAddr(object):
    @staticmethod
    def long2net(arg):
        if (arg <= 0 or arg >= 0xFFFFFFFF):
            raise ValueError("illegal netmask value", hex(arg))
        return 32 - int(round(math.log(0xFFFFFFFF - arg, 2)))

    @staticmethod
    def to_CIDR_notation(bytes_network, bytes_netmask):
        network = scapy.utils.ltoa(bytes_network)
        netmask = getIpAddr.long2net(bytes_netmask)
        net = "%s/%s" % (network, netmask)
        if netmask < 16:
            logger.warn("%s is too big. skipping" % net)
            return None

        return net

    @staticmethod
    def scan_and_print_neighbors(net, interface, timeout=1):
        logger.info("arping %s on %s" % (net, interface))
        macIpAddrPointer = {}
        try:
            ans, unans = scapy.layers.l2.arping(net, iface=interface, timeout=timeout, verbose=True)
            for s, r in ans.res:
                line = r.sprintf("%Ether.src%  %ARP.psrc%")
                try:
                    hostname = socket.gethostbyaddr(r.psrc)
                    line += " " + hostname[0]
                except socket.herror:
                    # failed to resolve
                    pass
                #logger.info(line)
                macAddr, ipAddr = line.split()
                macIpAddrPointer[macAddr] = ipAddr
        except socket.error as e:
            if e.errno == errno.EPERM:     # Operation not permitted
                logger.error("%s. Did you run as root?", e.strerror)
            else:
                raise
        return macIpAddrPointer


    @staticmethod
    def main():
        for network, netmask, _, interface, address in scapy.config.conf.route.routes:
            if network == 0 or interface == 'lo' or address == '127.0.0.1' or address == '0.0.0.0':
                continue
            if netmask <= 0 or netmask == 0xFFFFFFFF:
                continue
            net = getIpAddr.to_CIDR_notation(network, netmask)

            if interface != scapy.config.conf.iface:
                logger.warn("skipping {0}, scapy not supporting non primary network".format(net))
                continue

            if net:
                return getIpAddr.scan_and_print_neighbors(net, interface)

if __name__ == "__main__":
    pprint.pprint(getIpAddr.main())
