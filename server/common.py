# coding=utf-8
# 作用：通用方法

import os, zipfile, platform
import json
import hashlib
import subprocess
import qrcode

#压缩文件夹
def zip_dir(dirname, zipfilename):
    filelist = []
    if os.path.isfile(dirname):
        filelist.append(dirname)
    else :
        for root, dirs, files in os.walk(dirname):
            for name in files:
                filelist.append(os.path.join(root, name))
         
    zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED)
    for tar in filelist:
        arcname = tar[len(dirname):]
        zf.write(tar,arcname)
    zf.close()

#获取文件MD5
def getmd5(filename):  
    m = hashlib.md5()
    mfile = open(filename, 'rb')
    m.update(mfile.read())
    mfile.close()
    return m.hexdigest()

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


#获取连接字符串
def GetQRCodeInfo(nMethod, workdir, strIP, strPort):
    dataRoot = {}
    dataRoot['version'] = '2'
    dataRoot['IP'] = strIP
    dataRoot['port'] = strPort
    dataRoot['method'] = nMethod

    if nMethod == 1:
        datamd5 = getmd5(workdir)
        datasize = os.path.getsize(workdir)

        data = {}
        data['filename'] = workdir
        data['filesize'] = datasize
        data['filemd5'] = datamd5

        dataRoot['downData'] = data
    else:
        dataRoot['workdir'] = workdir
    
    QRCodeInfo = json.dumps(dataRoot, ensure_ascii=False)

    QRCodeInfo = QRCodeInfo.replace('\\\\', '/');
    QRCodeInfo = QRCodeInfo.replace('\\', '/');

    return QRCodeInfo

def GeneralQRCode(qrfile, nMethod, workdir, strIP, strPort):
    #生成连接信息
    QRCodeInfo = GetQRCodeInfo(nMethod, workdir, strIP, strPort)

    #生成二维码
    img = qrcode.make(QRCodeInfo)
    img.save(qrfile, 'JPEG')