# coding=utf-8
# 作用：微服务接口验证客户端

import os, hashlib
import requests
import json

#获取文件MD5
def getmd5(filename):
    m = hashlib.md5()
    mfile = open(filename, 'rb')
    m.update(mfile.read())
    mfile.close()
    return m.hexdigest()

fConnString = open('../server/temp/connectString.txt', 'r')
line = fConnString.readline()
fConnString.close()

connInfos = json.loads(line, encoding='utf-8')
print connInfos

connIP = connInfos['IP']
connPort = connInfos['port']
method = connInfos['method']

res = requests.get(url='http://' + connIP + ':' + connPort + '/connectsuccess')
print res


if (method == 1):
    #数据下载
    downData = connInfos['downData']

    urlString = 'http://' + connIP + ':' + connPort + '/download?fileid=' + downData['fileid']
    res = requests.get(url=urlString, stream=True)

    savefile = downData['fileid'] + ".zip"
    f = open(savefile, "wb")
    for chunk in res.iter_content(chunk_size=512):
        if chunk:
            f.write(chunk)

    f.close()

    print res
    datamd5 = getmd5(savefile)
    datasize = os.path.getsize(savefile)

    if (datamd5 != downData['filemd5'] or datasize != downData['filesize']):
        print '下载错误'
    else:
        print '下载成功'
else:
    #数据上传
    workdir = connInfos['workdir']
