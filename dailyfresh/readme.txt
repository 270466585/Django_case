使用制作简易电商网页
页面分为（按照制作顺序排序）：
一`df_user应用
模型类：userinfo

1.register：注册页
（1）用户名限制5-20位；且用户名不能已经存在（2）密码限制大于8位；
（3）两次密码输入相同（4）邮箱格式（5）勾选 同意”天天生鲜用户使用协议“
（6）提交时再次验证（1-5）
问题：（1）用户名不能存在 
2.login：登录页面
（1）用户名存在验证
（2）密码正确验证
（3）是否保存用户名 写cookie
（4）登陆后写入session，提高后期访问性能
问题：
（1）记住用户名未实现
（2）session应该也没有写进去   解决 证明写进去了
（3）输入错误后 错误信息能再次显示
3.info：个人信息
（1）基本信息 读取session
（2）最近浏览信息 
问题：后期添加浏览信息 暂时没有数据
4.order：全部订单
5.site ：收货地址
页面内post信息
问题：未能实现；

二 .df_goods
模型类：typeinfo goodsinfo
6. /：index.html   	首页 
(1)从数据库调数据
7.list：list.html	某一种商品列表页
（1）排序 默认（上架时间），人气，价格
（2）分页 不够分两页时，为什么会有两页？肯定有问题 迭代分页对象（Page） 
8.detail：detail.html	商品详情页
（1）js功能+- 修改文本框中的数据 无效

三. df_cart
9.cart： cart.html	购物车
四.df_order
10：place_order.html	提交订单页

day3
装饰器 user_decorator.login验证登陆与否：
问题：session已经写入，但是没法提出验证
cookie 总是写不上
但是最头上的显示 说明 session.user_name没有用成功
day4
1接入购物车 头部购物车；list中的购物车图标；detail中的加入购物车；
2购物车表 model 用户-购物车-商品
3购物车负责存储关系
day5
1结算 model
其中的ototal是为了减轻数据库的压力
2.订单对象的创建
day6
1全文检索：跟课间走
文件夹：templates-search-indexes-df_goods-goodsinfo_text.txt 对那些字段
进行检索
df_goods-search_indexes.py
2.jieba结巴分词 github
day7
1.部署到服务器  部署后 debug改为false allowed添加*
2. WSGI网站服务器网关接口；是一套规范，一种规定；
运行python的服务器（实际生成使用）
3.uWSGI 实现了wsgi的所有接口（一个遵守wsgi规范的软件），监听网卡端口，yunx
python
4.nginx
负载均衡 反向代理
client浏览器->nginx->>uwsgi->django下的python
5.nginx连接时
选择socket--停用http--默认80端口
静态文件找不到-> 
新建文件 /var/www/test7/static;
 (要有读写权限 sudo chmod 777 static)

采集静态文件 python manage.py collection
总结三步走：配置uwsgi nginx 静态文件





