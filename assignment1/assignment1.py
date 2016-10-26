#https://github.com/tensorflow/tensorflow/blob/master/tensorflow/examples/udacity/1_notmnist.ipynb

from __future__ import print_function
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import tarfile
from IPython.display import display, Image
from scipy import ndimage
from sklearn.linear_model import LogisticRegression
from six.moves.urllib.request import urlretrieve
from six.moves import cPickle as pickle
import data_utils

np.random.seed(133)
_DATA_LOC= "./data/"
train_filename = data_utils.maybe_download('notMNIST_large.tar.gz', _DATA_LOC, 247336696)
test_filename = data_utils.maybe_download('notMNIST_small.tar.gz', _DATA_LOC, 8458043)
print(train_filename)
print(test_filename)
train_folders = data_utils.maybe_extract(train_filename, _DATA_LOC)
test_folders = data_utils.maybe_extract(test_filename, _DATA_LOC)