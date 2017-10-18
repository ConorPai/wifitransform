# coding=utf-8
# 作用：微服务接口验证客户端

import time
import urllib.request
import requests

#统一进行消息处理
def showMessage(ip, port, strInfo):
    #命令行打印
    print(strInfo)
    #信息Url编码
    strInfoEncode = urllib.request.quote(strInfo)
    #信息传回服务端
    requests.get(url='http://' + ip + ':' + port + '/showinfo?info=' + strInfoEncode)

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
showMessage(ip, port, '客户端连接成功!')

# 数据下载
if (method == 'mztransformupload'):

    #提示正在上传文件
    showMessage(ip, port, '正在传输数据...')

    files = {'file': open('C:/Users/win7/Desktop/aa/aa.zip', 'rb')}
    res = requests.post('http://' + ip + ':' + port + '/upload', files=files)
    if (res.status_code == 200):
        showMessage(ip, port, '数据传输成功!')
    else:
        showMessage(ip, port, '数据传输错误!')


    #提示服务端上传完成
    requests.get(url='http://' + ip + ':' + port + '/uploaddone')

    #轮询获取服务端上传状态
    while (True):

        time.sleep(1)

        res = requests.get(url='http://' + ip + ':' + port + '/uploadstatus')
        
        if not res.status_code == 200:
            print('与服务端连接已断开')
            break

        if res.text == '0':
            print('服务端正在上传')
            continue
        elif res.text == '1':
            print('上传成功')
            break
        else:
            print('上传失败')
            break

    #提示服务端传输完成
    requests.get(url='http://' + ip + ':' + port + '/transformdone')
