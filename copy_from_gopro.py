#!/usr/bin/env python3

# Script to copy/move files from GoPro to a directory orderd by date directory

import os
import argparse
import datetime
import exifread
import shutil

def dir_path(string):
  if os.path.isdir(string):
    return string
  else:
    raise NotADirectoryError(string)

parser = argparse.ArgumentParser(description="")
parser.add_argument("-s", "--source", help="Source Direcory of GoPro images (recursive)", type=dir_path, required=True)
parser.add_argument("-d", "--destination", help="Destination directory where the images will be copied", type=dir_path, required=True)
parser.add_argument("-r", "--replace", help="Replace if file exists", action='store_true')

args = parser.parse_args()

source_directory = args.source
destination_directory = args.destination

count_copy = 0
count_move = 0
count_replace = 0
count_create = 0
count_skip = 0
count_error = 0

def get_datetime_exifread(filename):
  with open(filename, 'rb') as image_file:
    tags = exifread.process_file(image_file, details=False)

    retdate = None

    retdate = tags['Image DateTime'] if 'Image DateTime' in tags else retdate
    retdate = tags['DateTimeOriginal'] if 'DateTimeOriginal' in tags else retdate
    retdate = tags['GPS GPSDate'] if 'GPS GPSDate' in tags else retdate

    if retdate is None:
      # No exif data found - Linux only TODO: Windows
      return os.stat(filename).st_ctime
    retdate = datetime.datetime.strptime(str(retdate)[0:10], '%Y:%m:%d')

    return retdate

def print_stat():
  global count_skip, count_move, count_copy, count_create, count_replace, count_error
  print("Copy: " + str(count_copy) + " Move: " + str(count_move) + " Replace: " + str(count_replace) + " Skipped: " + str(count_skip) + " Created directories: " + str(count_create))

def copy_from(current_dir):
  global count_skip, count_move, count_copy, count_create, count_replace, count_error
  for filedir in os.listdir(current_dir):
    full_filedir = os.path.join(current_dir, filedir)

    if os.path.isfile(full_filedir) and full_filedir.upper().endswith('.JPG'):
      # print(full_filedir)
      # check date
      file_date = get_datetime_exifread(full_filedir)
      # create destination-directory
      target_dir = os.path.join(destination_directory, file_date.strftime('%Y-%m-%d'))
      target_file = os.path.join(target_dir, filedir)
      # check destination file
      if not os.path.exists(target_dir):
        print("Create destination directory " + target_dir)
        os.mkdir(target_dir)
      # copy/move
      if os.path.exists(target_file):
        if not args.replace:
          count_skip += 1
        else:
          shutil.copy(full_filedir,target_file)
          shutil.copystat(full_filedir,target_file)
          count_replace += 1
      else:
        shutil.copy(full_filedir,target_file)
        shutil.copystat(full_filedir,target_file)
        count_copy += 1
      # TODO copy file create

    elif os.path.isdir(full_filedir):
      # scan subdir
      copy_from(full_filedir)

copy_from(source_directory)
print_stat()
