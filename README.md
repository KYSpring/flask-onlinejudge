# flask-onlinejudge
基于flask,bootstrap框架的oj网站；python学习练手项目

## 2019/4/27 base_version上传完成 
这是一个flask学习实战练手项目； 
base_version里基本实现了oj的基本功能；
 
其中评测部分使用本地编译器编译和爬虫vjudge两种方法，并分成了两个单独的功能。

1）本地编译方法即通过本地服务器里配置的C++/C/Python2/python3环境进行编译运行，返回打印出编译结果和测试样例通过结果。

2）爬虫vjudge功能通过爬取poj网站的题目链接、爬虫模拟登录poj并提交程序、爬取运行结果数据这三步来实现。
 
此时的在线评测还处于比较初级的阶段，以后有机会再进行修改。


## 2019/5/10 增加了运行超时评测和POJ题目信息解析（利用beautifulsoup）

超时评测利用子进程轮询和killtask指令实现

题目解析利用beautifulsoup和自带html.parser解析器实现
