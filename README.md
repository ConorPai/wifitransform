# 局域网无线传输

之前在C#开发的桌面端与移动端进行数据传输时，只能使用数据线拷贝的方式，使用起来及其不便。特别是在安卓上使用windows默认的资源管理器会有刷新不及时的问题，只能使用应用宝之类的进行拷贝。所以需要实现无线传输功能，提高用户体验。

设计思路是桌面端使用python开发http服务，由移动端调用并进行数据双向传输。再由C#调用python脚本并完善整个流程。

流程概述：

1.数据下发：

1）桌面端准备好需要下发的数据

2）桌面端执行python脚本

3）python脚本压缩传输文件，并生成二维码，由桌面端显示。二维码信息：数据下发标识，服务版本号，端口号和可用IP集

4）移动端扫码并解析二维码信息

5）移动端从IP集中测试可连接的IP，桌面端接收到移动端的连接之后，隐藏二维码

6）移动端获取下发文件信息，并进行下载(目前是整个文件下载，以后考虑多线程分块下载，提高传输效率)

7）移动端下载成功，桌面端进行下发成功提示

8）移动端解压下发文件到具体的目录位置


2.数据上传：

1）桌面端执行python脚本

2）python脚本生成二维码，由桌面端显示。二维码信息：数据上传标识，服务版本号，端口号和可用IP集

3）移动端扫码并解析二维码信息

4）移动端从IP集中测试可连接的IP，桌面端接收到移动端的连接之后，隐藏二维码

5）移动端压缩需要上传的文件

6）移动端上传文件(目前是整个文件上传，以后考虑多线程分块上传，提高传输效率)

7）移动端上传成功

8）桌面端解压上传文件到临时目录，并完成数据合并逻辑

9）桌面端提示上传成功
