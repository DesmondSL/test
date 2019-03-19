# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 09:17:19 2017

@author: Admin

傅立叶变换的物理意义是将图像的灰度分布函数变换为图像的频率分布函数
"""


from __future__ import print_function
import tensorflow as tf
import os
#import matplotlib.pyplot as plt
#from PIL import Image
import numpy as np  
from skimage import io
#from skimage import img_as_ubyte
#import scipy
#from scipy.fftpack import dct
keep_prob=0.5 
 
tf.logging.set_verbosity(tf.logging.INFO)
def compute_accuracy(v_xs, v_ys):
    global regression#全局变量
    y_pre = sess.run(regression, feed_dict={xs: v_xs, keep_prob: 1})
    #accuracy=tf.reduce_mean(tf.reshape(tf.reduce_sum(tf.square(tf.subtract(ys,y_pre)),reduction_indices=[1]), shape=[-1,1]))
    #accuracy1=tf.reduce_mean(tf.square(tf.subtract(ys,y_pre)))
    
    accuracy=tf.sqrt(tf.reduce_sum(tf.square(ys-y_pre), 1))
    result = sess.run(accuracy, feed_dict={xs: v_xs, ys: v_ys, keep_prob: 1})
    return result

def weight_variable(shape):
    initial = tf.truncated_normal(shape, mean=0,stddev=0.01)#正态分布 stddev调整标准差 
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0.001, shape=shape)
    return tf.Variable(initial)

def conv2d(x, W):
    # stride [1, x_movement, y_movement, 1]
    # Must have strides[0] = strides[3] = 1
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

def max_pool_2x2(x):
    # stride [1, x_movement, y_movement, 1]
    return tf.nn.max_pool(x, ksize=[1,2,2,1], strides=[1,2,2,1], padding='SAME')
    
    

if __name__ == '__main__': 
# define placeholder for inputs to network

    xs = tf.placeholder(tf.float32, [None,2048],name='xs') # 272*448，列确定，行不确定
    ys = tf.placeholder(tf.float32, [None,784],name='ys')  
    keep_prob = tf.placeholder(tf.float32,name='keep_prob')
    #x_image = tf.reshape(xs, [-1,256,256, 1])# 图像转化为一个四维张量，第一个参数代表样本数量，-1表示不定第二三参数代表图像尺寸，最后一个参数代表图像通道数


   # Small epsilon value for the BN transform
    epsilon = 1e-3


# Layer 2 with BN, using Tensorflows built-in BN function
#w2_BN = tf.Variable(w2_initial)
#z2_BN = tf.matmul(l1_BN,w2_BN)
#batch_mean2, batch_var2 = tf.nn.moments(z2_BN,[0])
#scale2 = tf.Variable(tf.ones([100]))
#beta2 = tf.Variable(tf.zeros([100]))
#BN2 = tf.nn.batch_normalization(z2_BN,batch_mean2,batch_var2,beta2,scale2,epsilon)
#l2_BN = tf.nn.sigmoid(BN2)


   ## fc1 layer ##
    W_fc1 = weight_variable([2048, 4096])
    b_fc1 = bias_variable([4096])
    h_pool1_flat = tf.reshape(xs, [-1,2048])
    z1_BN = tf.matmul(h_pool1_flat, W_fc1)
    
    batch_mean1, batch_var1 = tf.nn.moments(z1_BN,[0])
    
    z1_hat = (z1_BN - batch_mean1) / tf.sqrt(batch_var1 + epsilon)
    
    scale1 = tf.Variable(tf.ones([4096]))
    beta1 = tf.Variable(tf.zeros([4096]))
    
    BN1 = scale1*z1_hat + beta1
    l1_BN = tf.nn.relu(BN1)   
   
    h_fc1_drop = tf.nn.dropout(l1_BN, keep_prob)
    
    
    
   ## fc3 layer ##
    W_fc3 = weight_variable([4096,2048])
    b_fc13 = bias_variable([2048])
    h_pool3_flat = tf.reshape(h_fc1_drop, [-1,4096])
    z3_BN = tf.matmul(h_pool3_flat, W_fc3)
    batch_mean3, batch_var3 = tf.nn.moments(z3_BN,[0])
    z3_hat = (z3_BN - batch_mean3) / tf.sqrt(batch_var3 + epsilon)
    scale3 = tf.Variable(tf.ones([2048]))
    beta3 = tf.Variable(tf.zeros([2048]))
    BN3 = scale3*z3_hat + beta3
    l3_BN = tf.nn.relu(BN3)
    h_fc3_drop = tf.nn.dropout(l3_BN, keep_prob)



   ## fc6 layer ##
    W_fc6 = weight_variable([2048,1024])
    b_fc16 = bias_variable([1024])
    h_pool6_flat = tf.reshape(h_fc3_drop, [-1,2048])
    z6_BN = tf.matmul(h_pool6_flat, W_fc6)
    batch_mean6, batch_var6 = tf.nn.moments(z6_BN,[0])
    z6_hat = (z6_BN - batch_mean6) / tf.sqrt(batch_var6 + epsilon)
    scale6 = tf.Variable(tf.ones([1024]))
    beta6 = tf.Variable(tf.zeros([1024]))
    BN6 = scale6*z6_hat + beta6
    l6_BN = tf.nn.relu(BN6)   
    h_fc6_drop = tf.nn.dropout(l6_BN, keep_prob) 


   ## fc7 layer ##
    W_fc7 = weight_variable([1024,1024])
    b_fc17 = bias_variable([1024])
    h_pool7_flat = tf.reshape(h_fc6_drop , [-1,1024])
    z7_BN = tf.matmul(h_pool7_flat, W_fc7)
    batch_mean7, batch_var7 = tf.nn.moments(z7_BN,[0])
    z7_hat = (z7_BN - batch_mean7) / tf.sqrt(batch_var7 + epsilon)
    scale7 = tf.Variable(tf.ones([1024]))
    beta7 = tf.Variable(tf.zeros([1024]))
    BN7= scale7*z7_hat + beta7
    l7_BN = tf.nn.relu(BN7)   
    #dropout
    h_fc7_drop = tf.nn.dropout(l7_BN, keep_prob)  



   ## fc8 layer ##
  #  W_fc8 = weight_variable([1024,1024])
 #   b_fc18 = bias_variable([1024])
 #   h_pool8_flat = tf.reshape(l7_BN  , [-1,1024])
#    z8_BN = tf.matmul(h_pool8_flat, W_fc8)
 #   batch_mean8, batch_var8 = tf.nn.moments(z8_BN,[0])
 ##   z8_hat = (z8_BN - batch_mean8) / tf.sqrt(batch_var8 + epsilon)
 #   scale8 = tf.Variable(tf.ones([1024]))
#    beta8 = tf.Variable(tf.zeros([1024]))
 #   BN8= scale8*z8_hat + beta8
 #   l8_BN = tf.nn.relu(BN8)
   # h_fc8_drop = tf.nn.dropout(l8_BN, keep_prob)


   ## fc4 layer ##
  #  W_fc4 = weight_variable([2048,2048])
 #   b_fc14 = bias_variable([2048])
 ##   z4_BN = tf.matmul(h_pool4_flat, W_fc4)
 #   batch_mean4, batch_var4 = tf.nn.moments(z4_BN,[0])
 #   z4_hat = (z4_BN - batch_mean4) / tf.sqrt(batch_var4 + epsilon)
  #  scale4 = tf.Variable(tf.ones([2048]))
 #   beta4 = tf.Variable(tf.zeros([2048]))
 #   BN4= scale4*z4_hat + beta4
  #  l4_BN = tf.nn.relu(BN4)
   # h_fc4_drop = tf.nn.dropout(l4_BN, keep_prob) 

   ## fc5 layer ##
    W_fc5 = weight_variable([1024,784])
    b_fc15 = bias_variable([784])
   # h_pool5_flat = tf.reshape(l4_BN, [-1,1024])
   # z5_BN = tf.matmul(h_pool5_flat, W_fc5)
  #  batch_mean5, batch_var5 = tf.nn.moments(z5_BN,[0])
  #  z5_hat = (z5_BN - batch_mean5) / tf.sqrt(batch_var5 + epsilon)
   # scale5 = tf.Variable(tf.ones([784]))
  #  beta5 = tf.Variable(tf.zeros([784]))
  #  regression= scale5*z5_hat + beta5
    #l5_BN = tf.nn.relu(BN5)
    regression = tf.matmul(h_fc7_drop ,W_fc5)+b_fc15
    #regression=tf.sigmoid(regression)
  #  regression=tf.clip_by_value(regression,0,255)
    #regression
    #W_conv8 = weight_variable([1,7,32,1]) # patch 5x5, in size 32, out size 1
    #b_conv8 = bias_variable([1])#feature map 28*28*1
    #h_conv8=tf.nn.relu(tf.nn.conv2d(h_pool7, W_conv8, strides=[1, 1, 1, 1], padding='VALID') + b_conv8)#激活函数能够给神经网络加入一些非线性因素，更好地解决较为复杂的问题。
   # h_conv8=tf.nn.conv2d(h_pool7, W_conv8, strides=[1, 1, 1, 1], padding='VALID') + b_conv8
    regression=tf.reshape(regression,[-1,784])
    
    
    # the error between prediction and real data 
    #mse = tf.reduce_mean(tf.reduce_sum(tf.square(tf.subtract(ys,regression)),reduction_indices=[1])) # loss,减法，平方。列相加，平均，开方
    #mse1 = tf.reduce_mean(tf.square(tf.subtract(ys,regression)))
    mse = tf.sqrt(tf.reduce_sum(tf.square(ys-regression), 1))
#reduce_sum() 就是求和,由于求和的对象是tensor,所以是沿着tensor的某些维度求和.reduction_indices是指沿tensor的哪些维度求和.0是行相加1是列相加
    train_step = tf.train.AdamOptimizer(0.001).minimize(mse)



    imgs3 = os.listdir('E:\\MachineLearning\\code\\recon\\1900\\')
    imgNum3= len(imgs3)
    data3 = np.empty((1900,2048),dtype="float32")
    for i in range (imgNum3):
       img=io.imread('E:\\MachineLearning\\code\\recon\\1900\\'+imgs3[i],as_grey=True)
       arr = np.asarray(img,dtype="float32")
       arr = [y for x in arr for y in x]
       data3[i,:]=arr
    train_s=data3/255
#train_s=2*data3/255-1


  
    imgs4 = os.listdir('E:\\MachineLearning\\code\\recon\\1900y\\')
    imgNum4= len(imgs4)
    data4 = np.empty((1900,784),dtype="float32")
    for i in range (imgNum4):
       img=io.imread('E:\\MachineLearning\\code\\recon\\1900y\\'+imgs4[i],as_grey=True)
       arr = np.asarray(img,dtype="float32")
       arr = [y for x in arr for y in x]
       data4[i,:]=arr
    train_y=data4/255
#train_y=2*data4/255-1 
#train_y=2*data4/255-1 
  
  #  train_y=2*data4/255-1




    saver = tf.train.Saver(write_version=tf.train.SaverDef.V2)   
    with tf.Session() as sess: 
        sess.run(tf.global_variables_initializer())  
        test_a=train_s[37*50:38*50]
        test_b=train_y[37*50:38*50]
       # print(test_a[0])
        for i in range(501):#训练2000次
           for j in range (37):#0到149
               temp_a=train_s[j*50:(j+1)*50]
        #   temp_a1=train_s[1*30:(1+1)*30]
               temp_b=train_y[j*50:(j+1)*50]
               train_step.run(session = sess, feed_dict = {xs:temp_a,ys:temp_b, keep_prob:0.7 }) 
            
              # print(compute_accuracy(temp_a, temp_a))
           print("step %d" %(i))
           print('train_accuracy  ')
           print(compute_accuracy(temp_a, temp_b))
          
           print("test accuracy ") 
           print(compute_accuracy(test_a,test_b))
           saver_path = saver.save(sess, "save2/model.ckpt")#H盘  
    ## 训练结束后，用测试集测试，并保存加噪图像、去噪图像  
           if i%20==0:
               
               y3 = sess.run(regression, feed_dict={xs:temp_a, keep_prob: 1})
               for k in range (50):
                   array3 = np.reshape(y3[k], newshape=[28,28])#原图第11854张               
                   y11=(array3)*255
                   max11=np.max(y11)
                   min11=np.min(y11)
                   y11=(y11-min11)/(max11-min11)*255
              # y1=(array+1)*255./2
                   y11= y11.astype(np.int)
               
                   #image11 = Image.fromarray(y11) 
                   io.imsave('E:\\MachineLearning\\code\\recon\\1900train\\' + str(k+1) +'_'+ str(i)+'.bmp', y11) 
               
               
               y = sess.run(regression, feed_dict={xs:test_a, keep_prob: 1})
               for k in range (50):
                   array = np.reshape(y[k], newshape=[28,28])#原图第11854张               
                   y1=(array)*255
                   max1=np.max(y1)
                   min1=np.min(y1)
                   y1=(y1-min1)/(max1-min1)*255
              # y1=(array+1)*255./2
                   y1= y1.astype(np.int)
                   
#                   image = Image.fromarray(y1) 
                   io.imsave('E:\\MachineLearning\\code\\recon\\1900test\\' + str(k+1) +'_'+ str(i)+'.bmp', y1)  
               
