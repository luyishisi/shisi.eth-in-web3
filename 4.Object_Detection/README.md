
本脚本用于生成可对接tensorflow model 中 Object_Detection 项目的record数据文件



你需要修改  Data_preprocessing.py 中的部分

一：指定数据源
img_root_dir = "./date_demo/jpgs/"

ans_root_dir = "./date_demo/ans/"

两个文件夹存放数据的格式为：

img_root_dir 存放要训练的图片数据，名字中的数字0_1504175671是唯一ID，对应另外一个文件夹中的答案

例如：ques0_1504175671.jpg 对应答案文件 ans0_1504175671.txt

ans_root_dir 存放要该ID对应的物体位置，其中的数字0_1504175671是唯一ID，对应另外一个文件夹中的图案

例如：每一行代表一个物体的标记，坐标是从左上角开始为X1,Y1,右下角为X2，Y2。后面是对物体特征的分类描述   

50 24 308 274 白色 猫

另外需要制定你的图片式什么格式的，在43行
...

二：设计你的分类

#****这个可以按照你的需求继续增加类别  在60行  可能需要处理下编码

color = t_list[4]#.decode("gb2312").encode("utf-8")

shape = t_list[5].replace("\r\n","")#.decode("gb2312").encode("utf-8")

if color == "白色" and shape == "猫": classes_text.append("white_cat"); classes.append(1)


三：对数据文件夹进行遍历，将所有数据导入文件

#*****93行

四：运行方式

python Data_preprocessing.py --output_path=out.record


五：官网说明
官网有点晦涩，主要还是自己折腾了半天才弄出来，就处理一下共享出来

https://github.com/tensorflow/models/blob/master/object_detection/g3doc/preparing_inputs.md
