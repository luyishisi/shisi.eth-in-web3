
使用TensorFlow去训练自己生成的验证码，
TensorFlow版本：
0.12  version：1.00


当前进度：

1：验证码自动生成---完成
使用命令 python gen_captcha.py 即可在同目录下生成验证码图片，，用于测试，同时被TensorFlow_cnn调用


2：进行训练 ：
python TensorFlow_cnn.py
当前程序设定一个成功率0.5或者0.7
我设置为当训练达到0.7 准确性就停止并且保留其模型。。
大概训练到 5k多次就能达到这个准确度。
训练30000次后就会达到 95%的准确度

3：测试：
完成训练后，自己测试模型准确度
python TensorFlow_cnn_test_model.py


新版说明：
加注释
