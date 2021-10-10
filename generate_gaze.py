import tensorflow as tf, numpy as np, keras as K, sys
import keras.layers as L
from keras.models import Model, Sequential # keras/engine/training.py
from IPython import embed
import ipdb
import json
import sys
import time
import os
import matplotlib.cm as cm
import seaborn as sns
import matplotlib.pylab as plt
from matplotlib.pyplot import imshow
import gaze.input_utils as IU, gaze.misc_utils as MU
from astropy.convolution import convolve
from astropy.convolution.kernels import Gaussian2DKernel

import os.path as path
import cv2
import copy
from scipy import misc

class CreateGaze():

    def __init__(self, rom: str, d1: int, d2: int) -> None:
        self.initialize_model(rom)
        self.dim1 = d1
        self.dim2 = d2

    def normalize(self, obs):
        max_val, min_val = np.max(obs), np.min(obs)
        if(max_val-min_val != 0):
            norm_map = (obs-min_val)/(max_val-min_val)
        else:
            norm_map = obs
        return norm_map

    def file_paths(self, rom: str):
        modelfile = path.join(os.getcwd(), 'gaze_models')
        meanfile  = path.join(os.getcwd(), 'gaze_models')

        extension = ""
        if rom == "mspacman":
            extension = "mspacman"
        elif rom == "revenge":
            extension = 'montezuma_revenge'
        elif rom == "spaceinvaders":
            extension = 'space_invaders'
        elif rom == "enduro":
            extension = 'enduro'
        elif rom == "seaquest":
            extension = 'seaquest'
        else:
            raise Exception(f"{rom} rom currently not supported")
        
        self.modelfile = path.join(modelfile, f'{extension}.hdf5')
        self.meanfile  = path.join(meanfile,  f'{extension}.mean.npy')
        return

    def initialize_model(self, rom: str) -> None:
        self.file_paths(rom)

        predict_mode = 1
        dropout = 0.5
        heatmap_shape = 84
        k = 4
        stride = 1
        SHAPE = (84,84,k)

        MU.BMU.save_GPU_mem_keras()
        MU.keras_model_serialization_bug_fix()

        ###############################
        # Architecture of the network #
        ###############################

        inputs=L.Input(shape=SHAPE)
        x=inputs # inputs is used by the line "Model(inputs, ... )" below

        conv1=L.Conv2D(32, (8,8), strides=4, padding='valid')
        x = conv1(x)
        print(conv1.output_shape)
        x=L.Activation('relu')(x)
        x=L.BatchNormalization()(x)
        x=L.Dropout(dropout)(x)

        conv2=L.Conv2D(64, (4,4), strides=2, padding='valid')
        x = conv2(x)
        print(conv2.output_shape)
        x=L.Activation('relu')(x)
        x=L.BatchNormalization()(x)
        x=L.Dropout(dropout)(x)

        conv3=L.Conv2D(64, (3,3), strides=1, padding='valid')
        x = conv3(x)
        print(conv3.output_shape)
        x=L.Activation('relu')(x)
        x=L.BatchNormalization()(x)
        x=L.Dropout(dropout)(x)

        deconv1 = L.Conv2DTranspose(64, (3,3), strides=1, padding='valid')
        x = deconv1(x)
        print(deconv1.output_shape)
        x=L.Activation('relu')(x)
        x=L.BatchNormalization()(x)
        x=L.Dropout(dropout)(x)

        deconv2 = L.Conv2DTranspose(32, (4,4), strides=2, padding='valid')
        x = deconv2(x)
        print(deconv2.output_shape)
        x=L.Activation('relu')(x)
        x=L.BatchNormalization()(x)
        x=L.Dropout(dropout)(x)         

        deconv3 = L.Conv2DTranspose(1, (8,8), strides=4, padding='valid')
        x = deconv3(x)
        print(deconv3.output_shape)
        #    x=L.Activation('relu')(x)
        #    x=L.BatchNormalization()(x)

        outputs = L.Activation(MU.my_softmax)(x)

        self.model=Model(inputs=inputs, outputs=outputs)

        opt=K.optimizers.Adadelta(lr=1.0, rho=0.95, epsilon=1e-08, decay=0.0)
        #opt=K.optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False) 

        self.model.compile(loss=MU.my_kld, optimizer=opt, metrics=[MU.NSS])
        #model.compile(loss=K.losses.kullback_leibler_divergence, optimizer=opt, metrics=[MU.NSS])

        self.model.load_weights(self.modelfile)

    def create_gaze_frame(self, atari_files: list, output_file: str, rom: str) -> None:
        mean = np.load(self.meanfile)

        stacked = []
        stacked_obs = np.zeros((84,84,4))

        for i in range(0, 4):
            frame_path = atari_files[i]
            obs = cv2.imread(frame_path)
            img_np = np.dot(obs, [0.299, 0.587, 0.114]) # convert to grayscale
            img_np = misc.imresize(img_np, [84, 84], interp='bilinear')
            img_np = np.expand_dims(img_np, axis=2)
            img_np = img_np.astype(np.float32) / 255.0
            img_np -= mean
            stacked_obs[:,:,i] = img_np.squeeze()

        stacked_obs = np.expand_dims(stacked_obs, axis=0)

        BATCH_SIZE = 1
        val_predict = self.model.predict(stacked_obs)


        # visualize predicted gaze heatmap
        output = self.normalize(val_predict.squeeze()) #1,84,84 -> 84,84
        cmap = cm.jet_r(output)[..., :3] * 255.0
        cmap = cmap.astype(np.float)
        img = misc.imresize(obs, [84, 84], interp='bilinear')
        hmap = (cmap.astype(np.float) + img.astype(np.float)) / 2
        hmap = np.uint8(hmap)

        # convolve output of network with gaussian filter
        output = misc.imresize(output, [self.dim1, self.dim2], interp='bilinear')
        m = cm.ScalarMappable(cmap='jet')
        pic = convolve(output, Gaussian2DKernel(x_stddev=1))
        pic = m.to_rgba(pic)[:,:,:3]

        # gaze heatmap
        #cv2.imwrite(output_file, np.uint8(pic*255.0))

        # saved heatmap
        #pic = cv2.imread('gaze/hm.png')
        #os.remove(output_file)
        temp = np.array(img)
        stor = temp[:,:,1].copy()
        temp[:,:,1] = temp[:,:,2]
        temp[:,:,2] = stor

        # blended
        #hmap = 0.5 * 255.0 * pic + 0.5 * np.uint8(255.0 * temp)
        hmap = 0.5 * 255.0 * pic + 0.5 * np.uint8(255.0 * obs)
        final = np.zeros((self.dim1, self.dim2 * 2, 3))
        #final[:,:160,:] = np.uint8(temp * 255.0)
        final[:,:self.dim2,:] = np.uint8(obs * 255.0)
        final[:,self.dim2:,:] = hmap
        
        cv2.imwrite(output_file, final)