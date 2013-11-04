# -*- coding:utf-8 -*-
#
# Sample HTTP Filtering list.
# - code by Jioh L. Jung (ziozzang@gmail.com)
#

from parsehttp import *
import re

# Sample bypass function.
def fooz(body):
  return body

# sample stream replace function.
# the target content is http stream, you must fix the length of contents size with padding.
def barz(buf):
  l = len(buf)
  # Replace stream
  buf = re.sub(r"<price>[^<]*</price>", "<price>0</price>", buf)
  # Build Padding
  s = l - len(buf)
  # Acquire target padding position
  p = buf.find("<list>")
  # Add Padding.
  buf = buf[:p] + " " * s + buf[p:]
  return buf

# Replace whole body.
def somereplace(body):
  # Acquire Header.
  hdr = getheaderpartonly(body)
  # Set Body Parts
  cnt = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
        <key>subscribed</key>
        <true/>
</dict>
</plist>"""
  # Replay Contents with header fixing.
  return fixcontentlength(hdr + "\r\n\r\n" + cnt)


# ------------------------------------------------------------------------------------------------------------
# Filters are dictionary format.
# - you can add any POST or GET type of URL, except "?queryparts"
# - if "http://foo/bar?doany" is target url, write only "http://foo/bar".
#

# Filter with URL Matching - Packet filtering
filter_url_pass = {
  "http://foo/uri" : fooz,
  "http://foo.com/request": somereplace,
}
# Filter with URL Matching - Fetch all and do filtering
filter_url_all = {
}

# Host is use when connect to server.
# - do not use resolved IP.
#

# Filter with Host Matching - Packet filtering
filter_host_pass = {
  "asdf.com": barz,
}
# Filter with Host Matching - Fetch all and do filtering
filter_host_all = {
}
