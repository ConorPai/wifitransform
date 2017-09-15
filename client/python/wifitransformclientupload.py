# coding=utf-8
# 作用：微服务接口验证客户端

import urllib.request
import requests

#扫码获得IP、端口号和服务类型
qrinfo = 'mztransformupload-1-8098-192.168.80.1:192.168.159.1:192.168.6.91:192.168.6.37:192.168.99.144'
method = qrinfo.split('-')[0]
version = qrinfo.split('-')[1]
port = qrinfo.split('-')[2]
ips = qrinfo.split('-')[3]

bConnect = False
iparray = ips.split(':')
for ip in iparray:
    try:
        #测试连接
        res = requests.get(url='http://' + ip + ':' + port + '/connectdone', timeout=1)
        if res.status_code == 200:
            bConnect = True
            break
    except:
        continue

if not bConnect:
    print('客户端连接失败!')
    exit()

#通知服务端连接成功
strInfo = '客户端连接成功!'
print(strInfo)
strInfoEncode = urllib.request.quote(strInfo)
requests.get(url='http://' + ip + ':' + port + '/showinfo?info=' + strInfoEncode)

# 数据下载
if (method == 'mztransformupload'):

    #提示正在上传文件
    strInfo = '正在传输数据...'
    print(strInfo)
    strInfoEncode = urllib.request.quote(strInfo)
    requests.get(url='http://' + ip + ':' + port + '/showinfo?info=' + strInfoEncode)

    files = {'file': open('C:/Users/win7/Desktop/aa/aa.zip', 'rb')}
    res = requests.post('http://' + ip + ':' + port + '/upload', files=files)
    if (res.status_code == 200):
        strInfo = '数据传输成功!'
        print(strInfo)
        strInfoEncode = urllib.request.quote(strInfo)
        requests.get(url='http://' + ip + ':' + port + '/showinfo?info=' + strInfoEncode)
    else:
        strInfo = '数据传输错误!'
        print(strInfo)
        strInfoEncode = urllib.request.quote(strInfo)
        requests.get(url='http://' + ip + ':' + port + '/showinfo?info=' + strInfoEncode)

    #提示服务端传输完成
    requests.get(url='http://' + ip + ':' + port + '/transformdone')
