#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#  pip install -i https://pypi.anaconda.org/pypi/simple urllib3
#  
from __future__ import print_function
import sys, math, re, types, urllib3, datetime, random, time, unicodedata, base64, socket
from bs4 import BeautifulSoup, SoupStrainer, Comment
import os, optparse
# python web_crawler.py -u http://clipartist.net
usage = 'Usage: %s -u <url>' % sys.argv[0]
parser=optparse.OptionParser()
parser.add_option('-u', '--url', help='url')
parser.add_option('-o', '--output', help='output file')
(opts, args) = parser.parse_args()
if opts.url is None:
  print (usage); print (sys.argv); sys.exit(1)

print ("url %s " % (opts.url))

def convert_accents(str):
  str= re.sub(r"^[ ]*\"", "",str)
  str= re.sub(r"\"[ ]*$", "",str)
  str= re.sub(r"Í", "e",str)
  str= re.sub(r"˙", "u",str)
  str= re.sub(r"Ë", "e",str)
  str= re.sub(r"»", "E",str)
  str= re.sub(r"Ì", "i",str)
  str= re.sub(r"¡", "A",str)
  str= re.sub(r"√", "A",str)
  str= re.sub(r"È", "e",str)
  str= re.sub(r"‡", "a",str)
  str= re.sub(r"‚", "a",str)
  str= re.sub(r"Ù", "o",str)
  str= re.sub(r"Á", "c",str)
  str= re.sub(r"Û", "o",str)
  str= re.sub(r"‘", "O",str)
  str= re.sub(r"„", "a",str)
  str= re.sub(r"·", "a",str)
  str= re.sub(r"ı", "o",str)
  str= re.sub(r" ", "E",str)
  str= re.sub(r"…", "E",str)
  str= re.sub(r"&quot;", "",str)
  str= re.sub(r"[ ]+", " ",str)
  return str

def clean_html(txt):
  # Remove all the HTML tags
  txt=re.sub(r"\n", ' ', txt)
  txt=re.compile(r'<[^>]+>').sub(' ',txt)
  txt=re.compile(r'&[^>]+;').sub(' ',txt)
  txt=re.compile(r'[ ]+').sub(' ',txt)
  return txt
  
  
def fetch_html(url):
  urls = []
  words = ''
  title = ''
  desc = ''
  keywords = ''
  body = ''
  status = ''
  server = ''
  content_type = ''
  last_modified = ''
  err=0
  url=re.compile(r"/$").sub('',url)
  url=re.compile(r"^http://").sub('',url)
  url = "http://" + url
  http = urllib3.PoolManager()
  response = http.request('GET',url)
  status = response.status
  server = response.headers['Server']
  content_type = response.headers['Content-Type']
  last_modified = response.headers['Date'] 
  print (response.status) # 200: ('OK', 'Request fulfilled, document follows'),
#  print class(response.status)  
  if response.status != 200:
    status = response.status   
    return (urls,body,title,desc,keywords,status,server,content_type,last_modified,err)
  print (response.headers)
 # print (response.data)   
  soup=BeautifulSoup(response.data, "lxml")
  try:
    title=clean_html(soup.html.head.title.string)
    title=convert_accents(title)
  except:
    title = ''  
  try:
    for meta in soup.head('meta'):
      ctxt = str(meta)
      pat = re.compile(r"meta[ ]*name[ ]*=[ ]*[\"]*key").findall(ctxt.lower())
      if pat:
        temp=re.compile(r"ontent[ ]*=[ ]*[\"]*").split(ctxt)
        if len(temp) > 1:
          keywords=temp[1]
          keywords=re.compile(r"[ ]*[\"]*[ ]*[/]*[>]").sub(' ',keywords)
          keywords=clean_html(keywords)
          keywords=convert_accents(keywords)
          keywords=keywords.strip()
      pat = re.compile(r"meta[ ]*name[ ]*=[ ]*[\"]*descrip").findall(ctxt.lower())
      if pat:
        temp=re.compile(r"ontent[ ]*=[ ]*[\"]*").split(ctxt)
        if len(temp) > 1:
          desc=temp[1]
          desc=re.compile(r"[ ]*[\"]*[ ]*[/]*[>]").sub(' ',desc)
          desc=convert_accents(desc)
          desc=desc.strip()
  except:
    err=1
  for comment in soup.findAll(text=lambda text:isinstance(text, Comment)):
    comment.extract()
  for script in soup.findAll('script'):
    script.extract()
  for link in soup.findAll('a', href=True):
    if len(link['href']) > 9:
      pat = re.compile(r'^http').findall(link['href'])
      if pat:
        href=re.compile(r"/$").sub('',link['href'])
        temp=re.compile(r"\.").split( href.lower())
        size = len(temp) -1
        urls.append(href)  
  body = soup.body(text=True)
  body = ' '.join(body)
  body=convert_accents(body)
  body=clean_html(body)
  try:
    body=unicodedata.normalize('NFKD',body).encode('ascii', 'ignore')
  except:
    err=2
  try:
    title=unicodedata.normalize('NFKD',title).encode('ascii', 'ignore')
  except:
    err=3       
  return (urls,body,title,desc,keywords,status,server,content_type,last_modified,err)

web_page=fetch_html(opts.url)
print (web_page)

      