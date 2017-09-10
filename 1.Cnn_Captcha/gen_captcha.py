#coding:utf-8
from captcha.image import ImageCaptcha  # pip install captcha
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import random,time,os

# 验证码中的字符, 就不用汉字了
number = ['0','1','2','3','4','5','6','7','8','9']
alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
ALPHABET = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

# 验证码一般都无视大小写；验证码长度4个字符
def random_captcha_text(char_set=number+alphabet+ALPHABET, captcha_size=4):
	''' 指定使用的验证码内容列表和长期 返回随机的验证码文本 '''
	captcha_text = []
	for i in range(captcha_size):
		c = random.choice(char_set)
		captcha_text.append(c)
	return captcha_text

def gen_captcha_text_and_image():
	'''生成字符对应的验证码 '''
	image = ImageCaptcha() #导入验证码包 生成一张空白图

	captcha_text = random_captcha_text() # 随机一个验证码内容
	captcha_text = ''.join(captcha_text) # 类型转换为字符串

	captcha = image.generate(captcha_text)
	#image.write(captcha_text, captcha_text + '.jpg')  # 写到文件

	#rm  =  'rm '+captcha_text + '.jpg'
	#os.system(rm)

	captcha_image = Image.open(captcha) #转换为图片格式
	captcha_image = np.array(captcha_image) #转换为 np数组类型

	return captcha_text, captcha_image

if __name__ == '__main__':
	# 测试
    while(1):
    	text, image = gen_captcha_text_and_image()
    	print 'begin ',time.ctime(),type(image)
    	f = plt.figure()
    	ax = f.add_subplot(111)
    	ax.text(0.1, 0.9,text, ha='center', va='center', transform=ax.transAxes)
    	plt.imshow(image)
    	plt.show() #显示，，取消注释并在30行取消写到文件的注释即可保存为文件
    	print 'end ',time.ctime()

	#print gen_captcha_text_and_image()
