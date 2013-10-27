"""
The ping service in pure Python.

Copyright (c) 2011-2013 "Johannes Findeisen and Rafael Timmerberg"

This file is part of Linspector (http://linspector.org).

Linspector is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

# http://code.activestate.com/recipes/409689-icmplib-library-for-creating-and-reading-icmp-pack/
import struct

from logging import getLogger

from linspector.services.service import Service

logger = getLogger(__name__)


class Packet(object):
    """Creates ICMPv4 and v6 packets.

    header
        two-item sequence containing the type and code of the packet,
        respectively.
    version
        Automatically set to version of protocol being used or None if ambiguous.
    data
        Contains data of the packet.  Can only assign a subclass of basestring
        or None.

    packet
        binary representation of packet.

    """

    header_table = {
                0 : (0, 4),
                #3 : (15, 4),  Overlap with ICMPv6
                3 : (15, None),
                #4 : (0, 4),  Deprecated by RFC 1812
                5 : (3, 4),
                8 : (0, 4),
                9 : (0, 4),
                10: (0, 4),
                11: (1, 4),
                12: (1, 4),
                13: (0, 4),
                14: (0, 4),
                15: (0, 4),
                16: (0, 4),
                17: (0, 4),
                18: (0, 4),

                1: (4, 6),
                2: (0, 6),
                #3 : (2, 6),  Overlap with ICMPv4
                #4 : (2, 6),  Type of 4 in ICMPv4 is deprecated
                4: (2, None),
                128: (0, 6),
                129: (0, 6),
                130: (0, 6),
                131: (0, 6),
                132: (0, 6),
                133: (0, 6),
                134: (0, 6),
                135: (0, 6),
                136: (0, 6),
                137: (0, 6),
             }

    def _setheader(self, header):
        """Set type, code, and version for the packet."""
        if len(header) != 2:
            raise ValueError("header data must be in a two-item sequence")
        type_, code = header
        try:
            max_range, version = self.header_table[type_]
        except KeyError:
            raise ValueError("%s is not a valid type argument" % type_)
        else:
            if code > max_range:
                raise ValueError("%s is not a valid code value for type %s" %\
                                     (type_, code))
            self._type, self._code, self._version = type_, code, version

    header = property(lambda self: (self._type, self._code), _setheader,
                       doc="type and code of packet")

    version = property(lambda self: self._version,
                        doc="Protocol version packet is using or None if "
                            "ambiguous")

    def _setdata(self, data):
        """Setter for self.data; will only accept a basestring or None type."""
        if not isinstance(data, basestring) and not isinstance(data, type(None)):
            raise TypeError("value must be a subclass of basestring or None, "
                            "not %s" % type(data))
        self._data = data

    data = property(lambda self: self._data, _setdata,
                    doc="data contained within the packet")

    def __init__(self, header=(None, None), data=None):
        """Set instance attributes if given."""
        #XXX: Consider using __slots__
        # self._version initialized by setting self.header
        self.header = header
        self.data = data
        self.type = None
        self.code = None

    def __repr__(self):
        return "<ICMPv%s packet: type = %s, code = %s, data length = %s>" % \
                (self.version, self.type, self.code, len(self.data))

    def create(self):
        """Return a packet."""
        # Kept as a separate method instead of rolling into 'packet' property so
        # as to allow passing method around without having to define a lambda
        # method.
        args = [self.header[0], self.header[1], 0]
        pack_format = "!BBH"
        if self.data:
            pack_format += "%ss" % len(self.data)
            args.append(self.data)
        # ICMPv6 has the IP stack calculate the checksum
        # For ambiguous cases, just go ahead and calculate it just in case
        if self.version == 4 or not self.version:
            args[2] = self._checksum(struct.pack(pack_format, *args))
        return struct.pack(pack_format, *args)

    packet = property(create,
                       doc="Complete ICMP packet")

    def _checksum(self, checksum_packet):
        """Calculate checksum"""
        byte_count = len(checksum_packet)
        #XXX: Think there is an error here about odd number of bytes
        if byte_count % 2:
            odd_byte = ord(checksum_packet[-1])
            checksum_packet = checksum_packet[:-1]
        else:
            odd_byte = 0
        two_byte_chunks = struct.unpack("!%sH" % (len(checksum_packet)/2),
                                        checksum_packet)
        total = 0
        for two_bytes in two_byte_chunks:
            total += two_bytes
        else:
            total += odd_byte
        total = (total >> 16) + (total & 0xFFFF)
        total += total >> 16
        return ~total

    def parse(cls, packet):
        """Parse ICMP packet and return an instance of Packet"""
        string_len = len(packet) - 4 # Ignore IP header
        pack_format = "!BBH"
        if string_len:
            pack_format += "%ss" % string_len
        unpacked_packet = struct.unpack(pack_format, packet)
        packetType, code, checksum = unpacked_packet[:3]
        try:
            data = unpacked_packet[3]
        except IndexError:
            data = None
        return cls((packetType, code), data)

    parse = classmethod(parse)


import socket
import time
import os


class PingResponse(object):
    def __init__(self, bufferLength, address, ident, seq, rtt):
        self.bufferLength = bufferLength
        self.address = address
        self.ident = ident
        self.seq = seq
        self.rtt = rtt

    def get_response_time(self):
        return self.rtt

    def __str__(self):
        return "%d bytes from %s: id=%s, seq=%u, rtt=%.3f ms" % \
               (self.bufferLength, self.address, self.ident, self.seq, self.rtt)


class PingService(Service):
    def __init__(self, **kwargs):
        super(PingService, self).__init__(**kwargs)
        self.dataLen = 56
        self.bufferSize = 1500

    def execute(self, host):
        self.ping(host)

    def ping(self, address):
        print "PING (%s): %d data bytes" % (address, self.dataLen)

        ## create socket
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('icmp'))
        s.connect((address, 22))

        ## setuid back to normal user

        processId = os.getpid()
        os.setuid(processId)

        base_packet = Packet((8, 0))

        seqNum = 0
        ## create ping packet
        pdata = struct.pack("!HHd", processId, seqNum, time.time())

        ## send initial packet
        base_packet.data = pdata
        s.send(base_packet.packet)

        ## recv packet
        buf = s.recv(self.bufferSize)
        current_time = time.time()

        ## parse packet; remove IP header first
        r = Packet.parse(buf[20:])

        ## parse ping data
        (ident, seq, timestamp) = struct.unpack("!HHd", r.data)

        ## calculate rounttrip time
        rtt = current_time - timestamp
        rtt *= 1000
        return PingResponse(len(buf), address, ident, seq, rtt)

    def parse_result(self, executionResult):
        fails = {}
        for host, pingResult in executionResult.items():
            for failKey, failVal in self.get_fails().items():
                respTime = pingResult.get_response_time()
                if int(failVal) > int(respTime):
                    fails[failKey] = pingResult
        return fails

    def handle_result(self, parseResult):
        for member in self.get_hostgroup().get_members():
            for failKey, pingResult in parseResult.items():
                for task in member.get_tasks():
                    if failKey == task.get_task_type():
                        task._execute()


def create(kwargs):
    return PingService(**kwargs)