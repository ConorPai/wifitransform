# coding=utf-8
# 作用：发布微服务，提供生成二维码扫码连接下载文件功能

import os, sys, uuid, platform
import json
import qrcode
import subprocess
from flask import Flask, request
from common import zip_dir, getmd5

app = Flask(__name__)

#临时目录
tempdir = 'temp'

#获取连接字符串
def GetConnInfo(nMethod, workdir, strIP, strPort):
    dataRoot = {}
    dataRoot['version'] = '2'
    dataRoot['IP'] = strIP
    dataRoot['port'] = strPort
    dataRoot['method'] = nMethod

    if nMethod == 1:
        datafile = tempdir + '/' + str(uuid.uuid1()) +'.zip'
        zip_dir(workdir, datafile)
        datamd5 = getmd5(datafile)
        datasize = os.path.getsize(datafile)

        data = {}
        data['filename'] = datafile
        data['filesize'] = datasize
        data['filemd5'] = datamd5

        dataRoot['downData'] = data
    else:
        dataRoot['workdir'] = workdir
    
    strConnInfo = json.dumps(dataRoot, ensure_ascii=False)

    strConnInfo = strConnInfo.replace('\\\\', '/');
    strConnInfo = strConnInfo.replace('\\', '/');

    return strConnInfo

#显示二维码图片
def showImage(filename):
    osName = platform.system()
    if osName == 'Windows':
        subprocess.Popen([filename], shell=True)
    elif osName == 'Linux':
        if subprocess.call(['which', 'gvfs-open'], stdout=subprocess.PIPE) == 0:
            subprocess.Popen(['gvfs-open', filename])
        elif subprocess.call(['which', 'shotwell'], stdout=subprocess.PIPE) == 0:
            subprocess.Popen(['shotwell', filename])
        else:
            raise
    elif osName == 'Darwin':
        subprocess.Popen(['open', filename])
    else:
        raise Exception('other system')

#主函数
def main():

    #获取命令行参数
    params = sys.argv

    if (len(params) == 1):
        params.append('1')
        params.append('/Users/paiconor/Downloads/数据下发')
        params.append('192.168.99.144')
        params.append('8000')

    if (len(params) <= 4):
        return

    #清理临时目录
    if os.path.exists(tempdir):
        __import__('shutil').rmtree(tempdir)
    os.mkdir(tempdir)

    #生成连接信息
    strConnInfo = GetConnInfo(int(params[1]), params[2], params[3], params[4])

    #生成二维码
    img = qrcode.make(strConnInfo)
    qrfile = tempdir + '/' + str(uuid.uuid1()) +'.jpg'
    img.save(qrfile, 'JPEG')

    showImage(qrfile)

    #启动服务
    app.run(host=params[3], port=int(params[4]))

main()