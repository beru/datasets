import pathlib
import urllib.request
import sys
import time

pathlib.Path('./list/').mkdir(parents=True, exist_ok=True)

lines = open("./valid_wnids.txt", "r").readlines()

base_url = 'http://www.image-net.org/api/text/imagenet.synset.geturls.getmapping?wnid='

for line in lines:
  wnid = line.split()[0]
  with urllib.request.urlopen(base_url + wnid) as u:
    with open(f'./list/{wnid}.txt', 'bw') as o:
      o.write(u.read())
  print(wnid)
  time.sleep(0.5)
