import os
import sys
import tarfile
import numpy as np
from six.moves.urllib.request import urlretrieve
from six.moves import cPickle as pickle

_URL = 'http://commondatastorage.googleapis.com/books1000/'
_LAST_PERCENT_REPORTED = None
_NUM_CLASSES = 10

def ensure_dir(f):
  d = os.path.dirname(f)
  if not os.path.exists(d):
      os.makedirs(d)

def download_progress_hook(count, blockSize, totalSize):
  """A hook to report the progress of a download. This is mostly intended for users with
  slow internet connections. Reports every 1% change in download progress.
  """
  global _LAST_PERCENT_REPORTED
  percent = int(count * blockSize * 100 / totalSize)

  if _LAST_PERCENT_REPORTED != percent:
    if percent % 5 == 0:
      sys.stdout.write("%s%%" % percent)
      sys.stdout.flush()
    else:
      sys.stdout.write(".")
      sys.stdout.flush()

    _LAST_PERCENT_REPORTED = percent

def maybe_download(filename, data_loc, expected_bytes, force=False):
  ensure_dir(data_loc)

  """Download a file if not present, and make sure it's the right size."""
  download_path = data_loc + filename
  if force or not os.path.exists(download_path):
    print('Attempting to download:', filename)
    filename, _ = urlretrieve(_URL + filename, download_path, reporthook=download_progress_hook)
    print('\nDownload Complete!')
  statinfo = os.stat(download_path)
  if statinfo.st_size == expected_bytes:
    print('Found and verified', download_path)
  else:
    raise Exception(
      'Failed to verify ' + download_path + '. Can you get to it with a browser?')
  return download_path

def maybe_extract(filename, dir, force=False):
  root = os.path.splitext(os.path.splitext(filename)[0])[0]  # remove .tar.gz
  if os.path.isdir(root) and not force:
    # You may override by setting force=True.
    print('%s already present - Skipping extraction of %s.' % (root, filename))
  else:
    print('Extracting data for %s. This may take a while. Please wait.' % root)
    tar = tarfile.open(filename)
    sys.stdout.flush()
    tar.extractall(dir)
    tar.close()
  data_folders = [
    os.path.join(root, d) for d in sorted(os.listdir(root))
    if os.path.isdir(os.path.join(root, d))]
  if len(data_folders) != _NUM_CLASSES:
    raise Exception(
      'Expected %d folders, one per class. Found %d instead.' % (
        _NUM_CLASSES, len(data_folders)))
  print(data_folders)
  return data_folders
