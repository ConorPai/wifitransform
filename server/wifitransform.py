# coding=utf-8
# 作用：发布微服务，提供生成二维码扫码连接下载文件功能

import os, sys, uuid, platform
import json
import qrcode
import subprocess
from flask import Flask, request
app = Flask(__name__)

#获取连接字符串
def GetConnInfo(nMethod, downDataDir, strIP, strPort):
    dataRoot = {}
    dataRoot['version'] = "1"
    dataRoot['IP'] = strIP
    dataRoot['port'] = strPort

    if nMethod == 1:
        listDownDatas = []
        GetDirFile(downDataDir, '', listDownDatas)
        dataRoot['downData'] = listDownDatas
    strConnInfo = json.dumps(dataRoot, ensure_ascii=False)

    strConnInfo = strConnInfo.replace("\\\\", "/");
    strConnInfo = strConnInfo.replace("\\", "/");

    return strConnInfo

#获取目录下的所有文件
def GetDirFile(parentDir, directParentDir, listFiles):
    for i in os.listdir(parentDir):
        curPath = os.path.join(parentDir, i)
        if os.path.isfile(curPath):
            filePath = os.path.join(directParentDir, i)
            listFiles.append(filePath)
        else:
            directParentDir2 = os.path.join(directParentDir, i)
            GetDirFile(curPath, directParentDir2, listFiles)

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
        params.append("1")
        params.append("/Users/paiconor/Downloads/数据下发")
        params.append("192.168.99.144")
        params.append("8000")

    if (len(params) <= 4):
        return

    #生成连接信息
    strConnInfo = GetConnInfo(int(params[1]), params[2], params[3], params[4])

    #生成二维码
    img = qrcode.make(strConnInfo)
    qrfile = str(uuid.uuid1()) +'.jpg'
    img.save(qrfile, 'JPEG')

    showImage(qrfile)

    #启动服务
    app.run(host=params[3], port=int(params[4]))

main()