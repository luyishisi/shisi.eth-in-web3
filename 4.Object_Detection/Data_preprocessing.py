#coding:utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import hashlib
import io
import logging
import os

from lxml import etree
import PIL.Image
import tensorflow as tf

from object_detection.utils import dataset_util
from object_detection.utils import label_map_util


flags = tf.app.flags
flags.DEFINE_string('output_path', '', 'Path to output TFRecord')
#flags.DEFINE_string('./', '', './')
FLAGS = flags.FLAGS

img_root_dir = "./date_demo/jpgs/"
ans_root_dir = "./date_demo/ans/"

#def create_tf_example(example):
def create_tf_example(img_url,ans_url):
  global img_root_dir,ans_root_dir
  # (user): Populate the following variables from your example.
  height = 480 # Image height
  width = 680 # Image width
  filename = img_url # Filename of the image. Empty if image is not from file

  encoded_image_data = None # Encoded image bytes

  with tf.gfile.GFile(img_root_dir +  filename, 'rb') as fid:
    encoded_jpg = fid.read()
  encoded_jpg_io = io.BytesIO(encoded_jpg)
  image = PIL.Image.open(encoded_jpg_io)

  #这里需要处理一下你的数据是什么格式的 # b'jpeg' or b'png'
  if image.format != 'JPEG':
    raise ValueError('Image format not JPEG')
  key = hashlib.sha256(encoded_jpg).hexdigest()
  image_format = b'jpeg' # b'jpeg' or b'png'

  f = open(ans_root_dir+ans_url)

  xmins = []; xmaxs = []; ymins = []; ymaxs = []; classes_text = []; classes = [];

  for i in f.readlines():
      #**************这里很重要，根据你的坐标系给出这个物体他的左上角的xy和右下角的xy
      t_list = i.split(" ")
      xmins.append(float(t_list[0])/width) # List of normalized left x coordinates in bounding box (1 per box)
      ymins.append(float(t_list[1])/height) # List of normalized left x coordinates in bounding box (1 per box)
      xmaxs.append(float(t_list[2])/width) # List of normalized left x coordinates in bounding box (1 per box)
      ymaxs.append(float(t_list[3])/height) # List of normalized left x coordinates in bounding box (1 per box)

      #这里看情况进行处理编码和处理文本的\n等符号，
      color = t_list[4].decode("gb2312").encode("utf-8")
      shape = t_list[5].replace("\r\n","").decode("gb2312").encode("utf-8")

      #****这个可以按照你的需求继续增加类别
      if color == "白色" and shape == "猫": classes_text.append("white_cat"); classes.append(1)

  #print xmins,ymins,xmaxs,ymaxs
  #print classes_text,classes

  tf_example = tf.train.Example(features=tf.train.Features(feature={
      'image/height': dataset_util.int64_feature(height),
      'image/width': dataset_util.int64_feature(width),
      'image/filename': dataset_util.bytes_feature(filename),
      'image/source_id': dataset_util.bytes_feature(filename),
      'image/key/sha256': dataset_util.bytes_feature(key.encode('utf8')),
      'image/encoded': dataset_util.bytes_feature(encoded_jpg),
      'image/format': dataset_util.bytes_feature(image_format),
      'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
      'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
      'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
      'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
      'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
      'image/object/class/label': dataset_util.int64_list_feature(classes),
  }))
  return tf_example

def main(_):
  writer = tf.python_io.TFRecordWriter(FLAGS.output_path)
  global img_root_dir,ans_root_dir
  # (user): Write code to read in your dataset to examples variable

  img_all_list = os.listdir(img_root_dir)
  ans_all_list = os.listdir(ans_root_dir)

  for img_url in img_all_list:
      #这里是要通过id来换算出ans的文件路径，
      ans_url = img_url.replace("ques","ans").replace("jpg","txt")

      tf_example = create_tf_example(img_url,ans_url)
      writer.write(tf_example.SerializeToString())

  writer.close()


if __name__ == '__main__':
  tf.app.run()
