# coding=utf-8
# 作用：通用方法

import io, os, sys, zipfile, platform, time
import hashlib
from pyqrcode import QRCode

serverVersion = '1'

#压缩文件夹
def zip_dir(dirname, zipfilename):
    filelist = []
    if os.path.isfile(dirname):
        filelist.append(dirname)
    else :
        for root, dirs, files in os.walk(dirname):
            for name in files:
                filelist.append(os.path.join(root, name))
         
    zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED, allowZip64=True)
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

try:
    b = u'\u2588'
    sys.stdout.write(b + '\r')
    sys.stdout.flush()
except UnicodeEncodeError:
    BLOCK = 'MM'
else:
    BLOCK = b

#在命令行中显示二维码
def print_cmd_qr(qrText, white=BLOCK, black='  ', enableCmdQR=True):
    blockCount = int(enableCmdQR)
    if abs(blockCount) == 0:
        blockCount = 1
    white *= abs(blockCount)
    if blockCount < 0:
        white, black = black, white
    sys.stdout.write(' '*50 + '\r')
    sys.stdout.flush()
    qr = qrText.replace('0', white).replace('1', black)
    sys.stdout.write(qr)
    sys.stdout.flush()

#显示二维码
def ShowQRCode(strIP, strPort, servertype, tempdir, showtype = 0):


    #生成二维码
    global serverVersion
    sInfo = servertype + '-' + serverVersion + '-' + strPort + '-' + strIP
    img = QRCode(sInfo)

    #将二维码保存成文件
    img.png(tempdir + '/qrcode.png', scale=5)

    #准备显示二维码
    qrStorage = io.BytesIO()
    img.png(qrStorage, scale=10)

    #直接显示二维码
    if showtype == 1:
        img.show()
    #二维码在命令行显示
    elif showtype == 2:
        osName = platform.system()
        if osName == 'Windows':
            enableCmdQR = 1
        else:
            enableCmdQR = -2

        print_cmd_qr(img.text(1), enableCmdQR=enableCmdQR)

#显示日志，用于与C#进行通信交互
def ShowLog(strTempDir, strLog):

    #判断是否存在读锁
    if os.path.exists(strTempDir + '/mzlockread'):

        #循环等到读锁释放
        while (True):
            time.sleep(0.5);
            if not os.path.exists(strTempDir + '/mzlockread'):
                break;

    #添加写锁
    lockfile = strTempDir + '/mzlockwrite'
    f = open(lockfile, "a+")
    f.close()

    #写入日志
    logfile = strTempDir + '/mzlog'
    f = open(logfile, "a+", encoding='utf8')
    f.write(strLog + '\n')
    f.close()

    #释放写锁
    os.remove(lockfile)

    #打印日志
    print(strLog)