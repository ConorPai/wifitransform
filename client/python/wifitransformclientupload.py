# coding=utf-8
# 作用：微服务接口验证客户端

import os
import requests

#扫码获得IP、端口号和服务类型
qrinfo = '127.0.0.1:8098-2'
connIPPort = qrinfo.split('-')[0]
method = qrinfo.split('-')[1]

#通知服务端连接成功
print('客户端连接成功!')
requests.get(url='http://' + connIPPort + '/showinfo?info=客户端连接成功!')

# 数据下载
if (method == '2'):

    #提示正在上传文件
    print('正在上传数据...')
    requests.get(url='http://' + connIPPort + '/showinfo?info=正在上传数据...')

    data = {'name':'uploadfile'}
    files = {'file': open('C:/Users/win7/Desktop/data/从化林地更新.zip', 'rb')}
    res = requests.post('http://' + connIPPort + '/upload', data=data, files=files)
    if (res.status_code == 200):
        print('数据上传成功!')
        requests.get(url='http://' + connIPPort + '/showinfo?info=数据上传成功!')
    else:
        print('数据上传错误!')
        requests.get(url='http://' + connIPPort + '/showinfo?info=数据上传错误!')

    #提示服务端传输完成
    requests.get(url='http://' + connIPPort + '/transformdone')

else:
    #数据上传
    todo = 'TODO'
