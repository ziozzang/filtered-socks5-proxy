# -*- coding:utf-8 -*-
#
# Utility Functions of HTTP packet filtering feture.
# - Code by Jioh L. Jung.(ziozzang@gmail.com)
#

import re

#HTTP 1.1 spec said that spliter is \r\n
def fixcontentlength(body, sp="\r\n"):
  s = len(sp)
  pos = body.find(sp*2)
  hdr = body[:pos]
  cnt = body[pos+s*2:]
  cntlen = len(cnt)
  hdr = re.sub(r"Content-Length[^\r\n]*", "Content-Length: %d" % (cntlen), hdr)
  return hdr + "\r\n\r\n" + cnt

# split content into header and body parts
def splitbody(body, sp="\r\n"):
  s = len(sp)
  pos = body.find(sp*2)
  hdr = body[:pos]
  cnt = body[pos+s*2:]
  return (hdr, cnt)

# Get Header lines list.
def getheaderslist(body):
  headers = []
  for i in body.splitlines():
    if len(i) == 0:
      break
    else:
      headers.append(i)
  return headers
  
# Get only Header Parts from contents.
def getheaderpartonly(body, sp="\r\n"):
  s = len(sp)
  pos = body.find(sp*2)
  hdr = body[:pos]
  return hdr

# Sample code for fixing stream data.
# - for match Content length, Resize of 'Content-Length' Header value.
def fixcontent_sample(body):
  hdr, bdy = splitbody(body)
  bdy = re.sub(r"<TagName>[^<]*</TagName>", "<TagName>0</TagName>", bdy)
  blen = len(bdy)
  hdr = re.sub(r"Content-Length[^\r\n]*", "Content-Length: %d" % (blen), hdr)
  return hdr + "\r\n\r\n" + cnt
