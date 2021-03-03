import pathlib
import urllib.request
import sys
import time
import os
import requests
import concurrent.futures
import json
from concurrent.futures import wait, ALL_COMPLETED

from os import listdir
from os.path import isfile, join

# https://markhneedham.com/blog/2018/07/15/python-parallel-download-files-requests/
def fetch_url(entry):
  path, uri = entry
  if not os.path.exists(path):
    try:
      r = requests.get(uri, stream=True, timeout=3.5)
      if r.status_code == 200:
        with open(path, 'wb') as f:
          for chunk in r:
            f.write(chunk)
    except Timeout:
      pass
  return path

list_path = 'list'
images_folder_path = 'images'

history_fh = open("history.txt", 'r+', encoding='utf-8')
history = {}
for line in history_fh.readlines():
  history[line.rstrip('\n')] = True

for fname in listdir(list_path):
  file_path = join(list_path, fname)
  if not isfile(file_path):
    continue
  
  wnid = os.path.splitext(fname)[0]
  
  if wnid in history:
    continue
    
  print(wnid, end='', flush=True)
  
  folder_path = os.path.join('.', images_folder_path, wnid)
  pathlib.Path(folder_path).mkdir(parents=True, exist_ok=True)
  
  entries = []
  lines = open(file_path, "r", encoding='utf-8').readlines()
  for line in lines:
    if not line.strip():
      break
    basename, url = line.split()
    _, file_extension = os.path.splitext(url)
    
    img_path = os.path.join(folder_path, basename + file_extension)
    if os.path.exists(img_path):
      continue
    entry = (img_path, url)
    entries.append(entry)
  
  start = time.time()
  with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    futures = [pool.submit(fetch_url, entry) for entry in entries]
    wait(futures)
  history_fh.write(wnid + '\n')
  history_fh.flush()
  print(f" : Elapsed Time: {time.time() - start}")
