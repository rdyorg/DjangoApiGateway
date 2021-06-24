# DesignArchitecture 系统设计架构

### 工程需求

* Mysql

> 数据存储

* Redis

> 优化查询，保存临时记录，主要是结构化的数据

### 启动信息

* 修改根目录下的config.py文件内的参数信息

* 启动脚本：**uvicorn django_api_gateway.asgi:application --reload --host 0.0.0.0 --port 10001**

### 重中之重

> 当前市面上的所有的api网关，如果有聚合服务，在对响应体进行聚合时，都是通过.操作进行配置，操作起来不方便

* 说明
    * 此方案对数据结构操作比较多，需要考虑到数据的操作的复杂性，空间和时间

* 解决方案
    * 采用可视化配置，对接口使用预请求，将响应体进行中文描述配置[一个api接口文档的业务]
    * 把多个接口的响应体进行简单json组装，加上唯一标识信息
    * 通过树形组件，对响应体进行结构重组
    * 通过添加函数组织，对响应体的内容进行二次操作，比如：
        * sum(data.age), max(data.age), min(), count(), len()
        * list(data.name) => 将当前对象下的某个属性单独抽离为另外一个类型为列表的数据

![Readme](https://github.com/RYD-Gateway/DjangoApiGateway/blob/master/images/微信图片_20210624164733.png)

### 设计说明

1.api服务，配置好对应内容之后，进行一次接口测试，将请求体和响应体进行格式化，对参数进行说明配置

1.1服务，包含正式环境和测试环境host信息，可以在上线时切换为正式环境

2.如果是转发，则直接将结果进行返回

3.如果是编排，需要添加步骤信息，每个步骤内的api接口使用协程进行请求，同一个步骤内的请求体和响应体无法共享使用，在完成一个步骤的配置后，将请求体和响应体进行命名，将结果信息进行可视化配置，方便后续步骤进行配置响应体结构

4.路由上包含上线和下线操作，路由path路径唯一

5.插件，作用在网关上的，对当前网关下的所有服务，对当前网关下的所有服务都有效

![Readme](https://github.com/RYD-Gateway/DjangoApiGateway/blob/master/images/微信图片_20210602231736.png)

![Readme](https://github.com/RYD-Gateway/DjangoApiGateway/blob/master/images/微信截图_20210618191053.png)
