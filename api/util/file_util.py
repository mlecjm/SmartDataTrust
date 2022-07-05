import csv
import yaml
import os
import errno
from pathlib import Path

"""
Author          : Neda Peyrone
Create Date     : 25-06-2021
File            : file_util.py
Purpose         : -
"""


def read_all_files(path):
  d = {}
  for p in Path(path).glob('*.graphql'):
    with p.open() as f:
      name = os.path.splitext(p.name)[0]
      d[name] = ' '.join([l.rstrip() for l in f])
  return d


def read_yaml_file(path):
  with open(path, "r") as ymlfile:
    cfg = yaml.safe_load(ymlfile)
    return cfg


def write_csv_file(path, file_name, data):
  __create_directories(path)
  with open(f'{path}/{file_name}', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(data)


def __create_directories(path):
  try:
    if not os.path.exists(path):
      os.makedirs(path)
  except OSError as e:
    if e.errno != errno.EEXIST:
      raise
