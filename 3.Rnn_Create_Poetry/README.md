
本项目最初学习于：

熊猫的博客：http://blog.topspeedsnail.com/archives/10542

参考：https://github.com/ryankiros/neural-storyteller（根据图片生成故事）

TensorFlow练习3:http://blog.topspeedsnail.com/archives/10443

http://karpathy.github.io/2015/05/21/rnn-effectiveness/

本帖代码移植自char-rnn：https://github.com/karpathy/char-rnn

使用rnn进行唐诗学习

然后main读取模型，生成新的唐诗

目前能在TensorFlow 0.11 中运行，0.12中因为函数移动而无法直接运行。

poetry.txt
是2w+的唐诗

<如何运行>

先运行python train.py

在持续运行的过程中，每7个batch计算会生成一个模型存于本文件中

待本机出现多个poetry.module-21 poetry.module-21.meta 则启动测试

python main.py

项目会返回使用当前模型计算的诗词：

海刚群笛古，崂复寒日闳。亊白眉釠抉，圹似望客枝。


虽然不怎么通顺不过还勉强能看。
