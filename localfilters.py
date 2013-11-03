# -*- coding:utf-8 -*-
from parsehttp import *
import re


def fooz(body):
  return body

def barz(buf):
  l = len(buf)
  buf = re.sub(r"<price>[^<]*</price>", "<price>0</price>", buf)
  # Build Padding
  s = l - len(buf)
  p = buf.find("<list>")
  buf = buf[:p] + " " * s + buf[p:]
  return buf

def somereplace(body):
  hdr, bdy = splitbody(body)
  cnt = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
        <key>subscribed</key>
        <true/>
</dict>
</plist>"""
  return fixcontentlength(hdr + "\r\n\r\n" + cnt)

filter_url_pass = {
  "http://foo/uri" : fooz,
  "http://foo.com/request": somereplace,
}
filter_url_all = {
}
filter_host_pass = {
  "asdf.com": barz,
}
filter_host_all = {
}
