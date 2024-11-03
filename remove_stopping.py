#!/usr/bin/env python3

# Script to remove/move double images and images without position

import os
import argparse
import exifread
from geopy import distance 

def dir_path(string):
  if os.path.isdir(string):
    return string
  else:
    raise NotADirectoryError(string)

parser = argparse.ArgumentParser(description="")
parser.add_argument("-p", "--directory", "--path", help="Direcory of GoPro images", type=dir_path, required=True)
parser.add_argument("-d", "--distance", help="Minimum distance between images to keep (in meters)", type=float, default=3)

args = parser.parse_args()

directory = args.directory
min_dist = args.distance

removed_dir = os.path.join(directory, 'remove')
no_position = os.path.join(directory, 'no_position')

last_keep_position = (0, 0)
last_file = ''
removed_cnt = 0
no_position_cnt = 0

if not os.path.exists(removed_dir):
  os.mkdir(removed_dir)
if not os.path.exists(no_position):
  os.mkdir(no_position)

def decimal_coords(coords, ref):
  decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600
  if ref == "S" or ref =='W' :
    decimal_degrees = -decimal_degrees
  return float(decimal_degrees)

def get_position_exifread(filename):
  with open(filename, 'rb') as image_file:
    tags = exifread.process_file(image_file, details=True)
  if 'GPS GPSLatitudeRef' in tags and 'GPS GPSLatitude' in tags:
    lat = decimal_coords(tags['GPS GPSLatitude'].values, tags['GPS GPSLatitudeRef'])
    lon = decimal_coords(tags['GPS GPSLongitude'].values, tags['GPS GPSLongitudeRef'])
    return (lat, lon)
  else:
    print ("No position in file " + filename)
    return None

for filename in sorted(os.listdir(directory)):
  f = os.path.join(directory, filename)
  if f.upper().endswith('.JPG') and os.path.isfile(f):
    cur_position = get_position_exifread(f)
    if cur_position is None:
      move_f = os.path.join(no_position, filename)
      os.rename(f, move_f)
      no_position_cnt += 1
      continue
    distance_2d = distance.distance(last_keep_position, cur_position).m

    if distance_2d > min_dist:
      last_keep_position = cur_position
      last_file = f
    else:
      print(filename + " to near: " + str(distance_2d))
      move_f = os.path.join(removed_dir, filename)
      os.rename(f, move_f)
      removed_cnt += 1 

print (str(removed_cnt) + " Moved Files to " + removed_dir)
print (str(no_position_cnt) + " Moved Files to " + no_position)
