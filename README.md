<center><font size=5>课题名：地下隧道掘进智能预测模型研究与构建</font></center>
[TOC]

### 一、Materials

* 吉林引松供水工程TBM3标段数据

* 盾构隧道数据***（暂未获取）***

* 其他benchmark datasets

 

### 二、Papers

1、相关背景资料

2、TBM掘进参数预测

3、基于先验知识的NN

4、注意力机制RNN

5、模型的可解释性



### 三、Techniques

模型训练：tensorflow/keras

前端：vue

后端：django/flask

 

### 四、Tasks

#### 1、阶段一：研究

**1）Tree-DNN —— 掘进参数预测模型**

了解tree结构的网络结构，搭建一个树结构的回归NN模型

* 模型搭建

* 模型训练

* 模型可解释性分析

**2）先验知识+attention mechanism RNN —— 掘进参数预测** 

了解先验知识如何优化神经网络的机制，了解注意力机制

- 数据预处理：上升段稳定段数据划分及时序数据提取

- 模型搭建

- 模型训练

**3）比对模型**

GBDT、GRNN（后期会有所增加）

#### 2、阶段二：成果可视化

前端：根据设计稿，采用vue框架完成前端搭建

后端：根据需求，完成前后端数据传递API以及调用模型的相关API

***PS：需要完成相关的需求设计文档***



目标：下学期一起写论文



### 五、展示界面

**前后端代码集成在BackEnd文件夹内**

```shell
cd BackEnd
cd SoftwareeEngineeringProject
cd mysite
python manage.py runserver
```

