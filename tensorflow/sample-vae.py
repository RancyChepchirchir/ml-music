# IPython log file
#import matplotlib
#matplotlib.use('Agg')

import numpy as np
import tensorflow as tf

import argparse
import time
import os
import cPickle
import util

from modelVAE import VAE

from matplotlib import pyplot as plt

data , means, stds = util.load_augment_data(util.loadf('../mp3/Kimiko Ishizaka - J.S. Bach- -Open- Goldberg Variations, BWV 988 (Piano) - 01 Aria.mp3'),1024)

vae = VAE(z_dim=256,net_size=2*256,chunk_samples=1024)
dirname = 'save-vae'
ckpt = tf.train.get_checkpoint_state(dirname)
vae.load_model(dirname)

x = np.zeros((2000,1024))
vz = np.random.randn(1,20)
z = np.random.randn(1,20)
z,zs = vae.encode(data[500:501,:1024])
zh = []
sh = []
for n in range(2000):
    z += 0.03*(-0.5*z + 3*np.random.randn(*z.shape))
    zh.append(np.sqrt(np.sum(z**2)))
    mu,s = vae.generate(z)
    sh.append(np.sqrt(np.exp(s)))
    x[n,:] = (mu+1.00*np.sqrt(np.exp(s))*np.random.randn(*mu.shape)).squeeze()

out = np.zeros((2*1024,2000))
out[:1024,:] = (x*stds+means).T
out[1024:,:] = 1-2*np.random.randint(2,size=(1024,2000))
sample_trace = util.write_data(np.minimum(out.T,1.1), fname = "out-vae.wav")
