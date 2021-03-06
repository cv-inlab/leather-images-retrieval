# -*- coding: utf-8 -*-

from __future__ import print_function

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage as nd

from skimage import data
from skimage.util import img_as_float
from skimage.filters import gabor_kernel

from tools.imtools import get_imlist
from skimage import io

# import PIL and pylab for plotting        
from PIL import Image
from pylab import *

import pickle

import math


def compute_feats(image, kernels):
    feats = np.zeros((len(kernels), 2), dtype=np.double)
    for k, kernel in enumerate(kernels):
        filtered = nd.convolve(image, kernel, mode='wrap')
        feats[k, 0] = filtered.mean()
        feats[k, 1] = filtered.var()
    return feats

# prepare filter bank kernels
kernels = []
for theta in range(4):                       # This parameter decides what kind of features the filter responds to.
    theta = theta / 4. * np.pi
    for sigma in (1, 3):       #  This parameter controls the width of the Gaussian envelope used in the Gabor kernel. Here are a few results obtained by varying this parameter.
        for frequency in (0.05, 0.25):
            kernel = np.real(gabor_kernel(frequency, theta=theta, sigma_x=sigma, sigma_y=sigma))  
            kernels.append(kernel)

imlist = get_imlist('./leatherImgs/')
# imlist = get_imlist('./Brodatz/')

# prepare reference features
feats = np.zeros((len(imlist), len(kernels), 2), dtype=np.double)
for index,imName in enumerate(imlist):
    print ("processing %s" % imName)
    img = img_as_float(np.asarray(Image.open(imName).convert('L')))
    feats[index, :, :] = compute_feats(img, kernels) # feats numpy.ndarray

# 进行归一化
feats = feats.reshape(len(imlist),feats.shape[1]*feats.shape[2])
for i in range(len(imlist)):
    meancolum = feats[:,i].mean()
    sigmacolum = math.sqrt(feats[:,i].var())
    sigmacolum = math.sqrt(feats[:,i].std())
    feats[:,i] = feats[:,i]-feats[:,i].mean()

outputFeature = open('gaborFeature.pkl', 'wb')
pickle.dump(feats, outputFeature)
outputFeature.close()
print("--- finish extracting feature---")