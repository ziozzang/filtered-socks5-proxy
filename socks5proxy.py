#!/usr/bin/python
# -*- coding:utf-8 -*-
#
# Socks5 Proxy Service with Contents Filtering Sample.
# This sample is for test purpose.
# - modification by Jioh L. Jung(ziozzang@gmail.com)
#
# Threaded Socks5 Server in Python
#
# Source: http://xiaoxia.org/2011/03/29/written-by-python-socks5-server/
#
#

#from gevent import monkey
#monkey.patch_all()

import socket, os, sys, select, SocketServer, struct, time
import re

class ThreadingTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer): pass
class Socks5Server(SocketServer.StreamRequestHandler):
    def handle_tcp(self, sock, remote):
        fdset = [sock, remote]
        self.marked = False
        self.filters = False
        self.filter_passthru = False
        self.reqtype = none
        self.cbuf = None
        while True:
            r, w, e = select.select(fdset, [], [])
            if sock in r:
                buf = sock.recv(4096)
                if not self.marked:
                   # build Packet Filter Marking
                   self.marked = True
                   s = buf.split("\n", 1)
                   if len(s) == 2:
                      q = s[0].split()
                      if q[0].lower() == "get" or q[0].lower() == "post":
                          if q[1].find("?") != -1:
                              self.base_uri = q[1].split("?")[0]
                          else:
                              self.base_uri = q[1]
                          self.uri = q[1]
                          self.reqtype = "http"
                          self.url = "http://" + self.addr + "/" + self.uri
                          self.base_url = "http://" + self.addr + "/" + self.base_uri
                          print self.url
                          print self.base_url
                   #debug
                   print buf
                   # Do Filtering Set
                if remote.send(buf) <= 0: break
            if remote in r:
                buf = remote.recv(4096)
                if self.filters and not self.filter_passthru:
                   # Exist Filter, but not passthru
                   if not buf:
                      if sock.send(self.cbuf) <= 0: break
                   if self.cbuf is None:
                      self.cbuf = buf
                   else:
                      self.cbuf = self.cbuf + buf
                elif self.filters and self.filter_passthru:
                   if not buf: break
                   #do Filtering
                   if sock.send(buf) <= 0: break
                else:
                   if not buf: break
                   if sock.send(buf) <= 0: break
    def handle(self):
        try:
            print 'socks connection from ', self.client_address
            sock = self.connection
            # 1. Version
            sock.recv(262)
            sock.send(b"\x05\x00");
            # 2. Request
            data = self.rfile.read(4)
            mode = ord(data[1])
            addrtype = ord(data[3])
            if addrtype == 1:       # IPv4
                addr = socket.inet_ntoa(self.rfile.read(4))
            elif addrtype == 3:     # Domain name
                addr = self.rfile.read(ord(sock.recv(1)[0]))
            port = struct.unpack('>H', self.rfile.read(2))
            reply = b"\x05\x00\x00\x01"
            try:
                if mode == 1:  # 1. Tcp connect
                    self.addr = addr
                    self.port = port[0]
                    remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    remote.connect((addr, port[0]))
                    print 'Tcp connect to', addr, port[0]
                else:
                    reply = b"\x05\x07\x00\x01" # Command not supported
                local = remote.getsockname()
                reply += socket.inet_aton(local[0]) + struct.pack(">H", local[1])
            except socket.error:
                # Connection refused
                reply = '\x05\x05\x00\x01\x00\x00\x00\x00\x00\x00'
            sock.send(reply)
            # 3. Transfering
            if reply[1] == '\x00':  # Success
                if mode == 1:    # 1. Tcp connect
                    self.handle_tcp(sock, remote)
        except socket.error:
            print 'socket error'
def main():
    server = ThreadingTCPServer(('', 1080), Socks5Server)
    server.serve_forever()

if __name__ == '__main__':
    main()
