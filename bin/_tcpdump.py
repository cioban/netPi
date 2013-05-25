#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
"""
Modulo:
"""
__author__ = 'Sergio Cioban Filho'
__version__ = '1.0'
__date__ = '25/05/2013 03:21:53 PM'

import datetime
import pcapy
import sys
from struct import unpack

def printByte(char_array):
    for TT in char_array:
        aux = "0x%02X" % ord(TT)
        sys.stdout.write(aux + " ")
    sys.stdout.write("\n")


class IPV4:
    protocols = {
        0x00: ['HOPOPT', 0],
        0x01: ['ICMP', 0],
        0x02: ['IGMP', 0],
        0x03: ['GGP', 0],
        0x04: ['IPv4', 0],
        0x05: ['ST', 0],
        0x06: ['TCP', 0],
        0x07: ['CBT', 0],
        0x08: ['EGP', 0],
        0x09: ['IGP', 0],
        0x0A: ['BBN-RCC-MON', 0],
        0x0B: ['NVP-II', 0],
        0x0C: ['PUP', 0],
        0x0D: ['ARGUS', 0],
        0x0E: ['EMCON', 0],
        0x0F: ['XNET', 0],
        0x10: ['CHAOS', 0],
        0x11: ['UDP', 0],
        0x12: ['MUX', 0],
        0x13: ['DCN-MEAS', 0],
        0x14: ['HMP', 0],
        0x15: ['PRM', 0],
        0x16: ['XNS-IDP', 0],
        0x17: ['TRUNK-1', 0],
        0x18: ['TRUNK-2', 0],
        0x19: ['LEAF-1', 0],
        0x1A: ['LEAF-2', 0],
        0x1B: ['RDP', 0],
        0x1C: ['IRTP', 0],
        0x1D: ['ISO-TP4', 0],
        0x1E: ['NETBLT', 0],
        0x1F: ['MFE-NSP', 0],
        0x20: ['MERIT-INP', 0],
        0x21: ['DCCP', 0],
        0x22: ['3PC', 0],
        0x23: ['IDPR', 0],
        0x24: ['XTP', 0],
        0x25: ['DDP', 0],
        0x26: ['IDPR-CMTP', 0],
        0x27: ['TP++', 0],
        0x28: ['IL', 0],
        0x29: ['IPv6', 0],
        0x2A: ['SDRP', 0],
        0x2B: ['IPv6-Route', 0],
        0x2C: ['IPv6-Frag', 0],
        0x2D: ['IDRP', 0],
        0x2E: ['RSVP', 0],
        0x2F: ['GRE', 0],
        0x30: ['MHRP', 0],
        0x31: ['BNA', 0],
        0x32: ['ESP', 0],
        0x33: ['AH', 0],
        0x34: ['I-NLSP', 0],
        0x35: ['SWIPE', 0],
        0x36: ['NARP', 0],
        0x37: ['MOBILE', 0],
        0x38: ['TLSP', 0],
        0x39: ['SKIP', 0],
        0x3A: ['IPv6-ICMP', 0],
        0x3B: ['IPv6-NoNxt', 0],
        0x3C: ['IPv6-Opts', 0],
        0x3D: ['Any host internal protocol', 0],
        0x3E: ['CFTP', 0],
        0x3F: ['Any local network', 0],
        0x40: ['SAT-EXPAK', 0],
        0x41: ['KRYPTOLAN', 0],
        0x42: ['RVD MIT', 0],
        0x43: ['IPPC', 0],
        0x44: ['Any distributed file system ', 0],
        0x45: ['SAT-MON SATNET', 0],
        0x46: ['VISA', 0],
        0x47: ['IPCV', 0],
        0x48: ['CPNX', 0],
        0x49: ['CPHB', 0],
        0x4A: ['WSN', 0],
        0x4B: ['PVP', 0],
        0x4C: ['BR-SAT-MON', 0],
        0x4D: ['SUN-ND', 0],
        0x4E: ['WB-MON', 0],
        0x4F: ['WB-EXPAK', 0],
        0x50: ['ISO-IP', 0],
        0x51: ['VMTP', 0],
        0x52: ['SECURE-VMTP', 0],
        0x53: ['VINES', 0],
        0x54: ['TTP', 0],
        0x54: ['IPTM', 0],
        0x55: ['NSFNET-IGP', 0],
        0x56: ['DGP', 0],
        0x57: ['TCF', 0],
        0x58: ['EIGRP', 0],
        0x59: ['OSPF', 0],
        0x5A: ['Sprite-RPC', 0],
        0x5B: ['LARP', 0],
        0x5C: ['MTP Multicast Transport Protocol', 0],
        0x5D: ['AX.25', 0],
        0x5E: ['IPIP', 0],
        0x5F: ['MICP', 0],
        0x60: ['SCC-SP', 0],
        0x61: ['ETHERIP', 0],
        0x62: ['ENCAP', 0],
        0x63: ['Any private encryption scheme', 0],
        0x64: ['GMTP', 0],
        0x65: ['IFMP', 0],
        0x66: ['PNNI', 0],
        0x67: ['PIM', 0],
        0x68: ['ARIS', 0],
        0x69: ['SCPS', 0],
        0x6A: ['QNX', 0],
        0x6B: ['A/N', 0],
        0x6C: ['IPComp', 0],
        0x6D: ['SNP', 0],
        0x6E: ['Compaq-Peer', 0],
        0x6F: ['IPX-in-IP', 0],
        0x70: ['VRRP', 0],
        0x71: ['PGM', 0],
        0x72: ['Any 0-hop protocol', 0],
        0x73: ['L2TP', 0],
        0x74: ['DDX', 0],
        0x75: ['IATP', 0],
        0x76: ['STP', 0],
        0x77: ['SRP', 0],
        0x78: ['UTI', 0],
        0x79: ['SMP', 0],
        0x7A: ['SM', 0],
        0x7B: ['PTP', 0],
        0x7C: ['IS-IS over IPv4', 0],
        0x7D: ['FIRE', 0],
        0x7E: ['CRTP', 0],
        0x7F: ['CRUDP', 0],
        0x80: ['SSCOPMCE', 0],
        0x81: ['IPLT', 0],
        0x82: ['SPS', 0],
        0x83: ['PIPE', 0],
        0x84: ['SCTP', 0],
        0x85: ['FC', 0],
        0x86: ['RSVP-E2E-IGNORE', 0],
        0x87: ['Mobility Header', 0],
        0x88: ['UDP Lite', 0],
        0x89: ['MPLS-in-IP', 0],
        0x8A: ['manet', 0],
        0x8B: ['HIP', 0],
        0x8C: ['Shim6', 0],
        0xFE: ['Unknown', 0],
    }
    ip_pkt = {
        'version': None,
        'ihl': None,
        'dscp': None,
        'ecn': None,
        'len': None,
        'identification': None,
        'flags': None,
        'fragment_offset': None,
        'ttl': None,
        'protocol': None,
        'checksum': None,
        'ip_src': None,
        'ip_dst': None,
        'options': None,
        'payload': None,
    }
    ip_data = {
        'byte_counter': 0,
        'ihl_counter': 0,
        'payload_byte_counter': 0,
    }

    def set_ip_pkt(self, received_data):
        data = received_data
        self.ip_pkt['version'] = (ord(data[0]) & 0xF0) >> 4
        self.ip_pkt['ihl'] = ord(data[0]) & 0x0F
        data = data[1:]
        self.ip_data['ihl_counter'] += self.ip_pkt['ihl']

        self.ip_pkt['dscp'] = (ord(data[0]) & 0xFC) >> 2
        self.ip_pkt['ecn'] = ord(data[0]) & 0x03
        data = data[1:]

        self.ip_pkt['len'] = unpack("!H", data[:2])[0]
        data = data[2:]
        self.ip_data['byte_counter'] += self.ip_pkt['len']

        self.ip_pkt['identification'] = unpack("!H", data[:2])[0]
        data = data[2:]

        self.ip_pkt['flags'] = (ord(data[0]) & 0xE0) >> 5
        self.ip_pkt['fragment_offset'] = unpack("!H", data[:2])[0] & 0x1FFF
        data = data[2:]

        self.ip_pkt['ttl'] = ord(data[0])
        data = data[1:]

        self.ip_pkt['protocol'] = ord(data[0])
        data = data[1:]

        self.ip_pkt['checksum'] = unpack("!H", data[:2])[0]
        data = data[2:]

        self.ip_pkt['ip_src'] = data[:4]
        data = data[4:]

        self.ip_pkt['ip_dst'] = data[:4]
        data = data[4:]

        if self.ip_pkt['ihl'] > 5:
            self.ip_pkt['options'] = unpack("!L", data[:4])[0]
            data = data[4:]

        self.ip_pkt['payload'] = data
        self.ip_data['payload_byte_counter'] += len(data)

    def ip_protocol_count(self):
        try:
            proto_data = self.protocols[self.ip_pkt['protocol']]
        except KeyError:
            proto_data = self.protocols[0xFE]

        proto_data[1] += 1

    def __init__(self, received_data):
        self.set_ip_pkt(received_data)
        self.ip_protocol_count()


class TCPDUMP:
    ethertypes = {
        0x0800: ['IPv4', 0, IPV4],
        0x0806: ['ARP', 0, None],
        0x0842: ['Wake-on-LAN', 0, None],
        0x22F3: ['IETF TRILL Protocol', 0, None],
        0x6003: ['DECnet Phase IV', 0, None],
        0x8035: ['Reverse ARP', 0, None],
        0x809B: ['AppleTalk', 0, None],
        0x80F3: ['AppleTalk ARP', 0, None],
        0x8100: ['VLAN-tagged', 0, None],
        0x8137: ['IPX', 0, None],
        0x8138: ['IPX', 0, None],
        0x8204: ['QNX Qnet', 0, None],
        0x86DD: ['IPv6', 0, None],
        0x8808: ['Ethernet flow control', 0, None],
        0x8809: ['Slow Protocols (IEEE 802.3)', 0, None],
        0x8819: ['CobraNet', 0, None],
        0x8847: ['MPLS unicast', 0, None],
        0x8848: ['MPLS multicast', 0, None],
        0x8863: ['PPPoE Discovery Stage', 0, None],
        0x8864: ['PPPoE Session Stage', 0, None],
        0x8870: ['Jumbo Frames', 0, None],
        0x887B: ['HomePlug 1.0 MME', 0, None],
        0x888E: ['IEEE 802.1X', 0, None],
        0x8892: ['PROFINET Protocol', 0, None],
        0x889A: ['SCSI over Ethernet', 0, None],
        0x88A2: ['ATA over Ethernet', 0, None],
        0x88A4: ['EtherCAT', 0, None],
        0x88A8: ['802.1ad & IEEE 802.1aq', 0, None],
        0x88AB: ['Ethernet Powerlink', 0, None],
        0x88CC: ['LLDP', 0, None],
        0x88CD: ['SERCOS', 0, None],
        0x88E1: ['HomePlug AV MME', 0, None],
        0x88E3: ['Media Redundancy Protocol (IEC62439-2)', 0, None],
        0x88E5: ['MAC security (IEEE 802.1AE)', 0, None],
        0x88F7: ['Precision Time Protocol (IEEE 1588)', 0, None],
        0x8902: ['IEEE 802.1ag', 0, None],
        0x8906: ['FCoE', 0, None],
        0x8914: ['FCoE Initialization Protocol', 0, None],
        0x8915: ['RDMA over Converged Ethernet (RoCE)', 0, None],
        0x9000: ['Ethernet Configuration Testing Protocol', 0, None],
        0x9100: ['Q-in-Q', 0, None],
        0xCAFE: ['Veritas Low Latency Transport (LLT)', 0, None],
        0x0000: ['Unkown', 0, None],
    }

    ethernet_data = {
        'pkt_couter': 0,
        'byte_counter': 0,
    }

    def __init__(self, iface=None, dumpfile=None, dumptime=0, dumpsize=0):
        self.iface = iface
        self.dumpfile = dumpfile
        self.dumptime = dumptime
        self.dumpsize = dumpsize
        self.dumper = None
        self.cap = None
        self.pkt_couter = 0

    def pkt_handler(self, hdr, received_data):
        data = received_data

        self.ethernet_data['pkt_couter'] += 1
        self.ethernet_data['byte_counter'] += hdr.getlen()

        mac_dst = data[:6]
        data = data[6:]

        mac_src = data[:6]
        data = data[6:]

        ethertype = unpack("!H", data[:2])[0]
        data = data[2:]

        try:
            ethertype_data = self.ethertypes[ethertype]
        except KeyError:
            ethertype_data = self.ethertypes[0x0000]

        ethertype_data[1] += 1
        if ethertype_data[2] is not None:
            ethertype_function = ethertype_data[2]
            ethertype_function(data)

    def main(self):
        # Parse flags
        # Arguments here are:
        # device
        # snaplen (maximum number of bytes to capture _per_packet_)
        # promiscious mode (1 for true)
        # timeout (in milliseconds)
        self.cap = pcapy.open_live(self.iface, 1518, 1, 0)

        try:
            self.cap.loop(0, self.pkt_handler)
        except KeyboardInterrupt:
            print 'shutting down'


if __name__ == "__main__":
    tcpdump = TCPDUMP(iface='eth0')
    tcpdump.main()
    from pprint import pprint
    for ether, DATA in tcpdump.ethertypes.iteritems():
        if DATA[1] > 0:
            print('%s: %d' % (DATA[0], DATA[1]))
    for proto, DATA in IPV4.protocols.iteritems():
        if DATA[1] > 0:
            print('%s: %d' % (DATA[0], DATA[1]))
    pprint(tcpdump.ethernet_data)
    pprint(IPV4.ip_data)

