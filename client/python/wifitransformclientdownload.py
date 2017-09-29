# coding=utf-8
# 作用：微服务接口验证客户端

import os, hashlib
import requests
import json, urllib.request

#获取文件MD5
def getmd5(filename):
    m = hashlib.md5()
    mfile = open(filename, 'rb')
    m.update(mfile.read())
    mfile.close()
    return m.hexdigest()

#统一进行消息处理
def showMessage(ip, port, strInfo):
    #命令行打印
    print(strInfo)
    #信息Url编码
    strInfoEncode = urllib.request.quote(strInfo)
    #信息传回服务端
    requests.get(url='http://' + ip + ':' + port + '/showinfo?info=' + strInfoEncode)


#扫码获得IP、端口号和服务类型(测试时写死)
qrinfo = 'mztransformdownload-1-8098-192.168.80.1:192.168.159.1:192.168.6.91:192.168.6.37:192.168.99.144'
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
if (method == 'mztransformdownload'):

    #获取下载文件信息
    res = requests.get(url='http://' + ip + ':' + port + '/downloadfileinfo')
    fileinfo = json.loads(res.content)

    #下载文件
    urlString = 'http://' + ip + ':' + port + '/download?fileid=' + fileinfo['fileid']
    res = requests.get(url=urlString, stream=True)

    #提示正在下载文件
    showMessage(ip, port, '正在下载数据...')

    #文件保存(测试时写死)
    savefile = '/Users/paiconor/PycharmProjects/wifitransform/wifitransform/client/python/' + fileinfo['fileid'] + ".zip"
    f = open(savefile, "wb")
    fsize = fileinfo['filesize']
    csize = int(fsize / 20)
    tsize= 0
    for chunk in res.iter_content(chunk_size=csize):
        if chunk:
            f.write(chunk)
            tsize += len(chunk)
            strmsg = '下载完成%.2f%%' % (float(int(tsize * 10000.0 / fsize)) / 100.0)
            print(strmsg)

    f.close()

    #验证文件大小和MD5，是否与服务端一致
    datamd5 = getmd5(savefile)
    datasize = os.path.getsize(savefile)

    if (datamd5 != fileinfo['filemd5'] or datasize != fileinfo['filesize']):
        showMessage(ip, port, '数据下载错误!')
    else:
        showMessage(ip, port, '数据下载成功!')

    #提示服务端传输完成
    requests.get(url='http://' + ip + ':' + port + '/transformdone')