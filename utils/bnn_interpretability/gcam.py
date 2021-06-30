import matplotlib.pyplot as plt
import numpy as np
import scipy as scp
from scipy import misc
from PIL import Image
import tensorflow as tf
import os

# Optional GPU setup
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
config = tf.ConfigProto()
config.log_device_placement = False
config.gpu_options.allow_growth = True
config.gpu_options.per_process_gpu_memory_fraction = 0.1

# Input raw image for CAM overlay (32x32 pixels)
raw_image = Image.open("/data/test_in.png")

# Extract gradients from training toolbox (e.g. Pytorch/Brevitas, Theano/BNN) as numpy (*.npz) files
# Gradients should be dy_prediction/dx_Activation, where x_Activation are the activations of the Conv. layer to be interpreted by CAM

grad_npz = np.load("/data/cnv/output_cam_grad_rsh.npz")
output_activations_rsh_npz = np.load("/data/cnv/output_activations_rsh.npz")
grad_feed = grad_npz["arr_0"]
act_feed = output_activations_rsh_npz["arr_0"]

# Shape of Conv. layer output
act = tf.placeholder(dtype=tf.float32, shape=[5, 5, 128])
grad = tf.placeholder(dtype=tf.float32, shape=[5, 5, 128])
grad_mean = tf.reduce_mean(grad, axis=(0, 1))

a_m = tf.image.resize_images(act, (32, 32), tf.image.ResizeMethod.BICUBIC)
cam = tf.nn.conv2d(tf.expand_dims(a_m, axis=0), tf.expand_dims(tf.expand_dims(tf.expand_dims(grad_mean, axis=0), axis=0), axis=-1), strides=[1, 1, 1,1],padding='SAME')

# Init Graph
global_init = tf.global_variables_initializer()
local_init = tf.local_variables_initializer()
init = tf.initialize_all_variables()

# Session
with tf.Session(config=config) as sess:
    sess.run(global_init)
    sess.run(local_init)
    sess.run(init)

    sess_output = sess.run(cam, feed_dict={act:act_feed,grad:grad_feed})

    sess_output = sess_output.reshape((32,32))

    cm = plt.get_cmap('jet', lut=255)
    rescaled_h_m = np.interp(sess_output, (sess_output.min(), sess_output.max()), (0, 255)).astype(np.uint8)
    colored_image = cm(rescaled_h_m)
    scale_colored_image = (colored_image[:, :, :3] * 255)
    im = Image.fromarray(scale_colored_image[:, :, :3].astype(np.uint8))
    scp.misc.imsave(os.path.join('/data/cam_out/', 'heat_map_%d.png' %1), im)
    scp.misc.imsave(os.path.join('/data/cam_out/', 'raw_image.png'), raw_image)
    background = Image.open(os.path.join('/data/cam_out/', 'raw_image.png'))
    overlay = Image.open(os.path.join('/data/cam_out/', 'heat_map_%d.png'%1))
    background = background.convert("RGBA")
    overlay = overlay.convert("RGBA")

    # Upsample background if it is smaller than overlay
    if background.size[0] < overlay.size[0]:
        background = background.resize(overlay.size, Image.BILINEAR)

    new_img = Image.blend(background, overlay, 0.5)
    new_img.save(os.path.join('/data/cam_out/', 'overlay_%d.png' %1), "PNG")

