# coding=utf-8
# 作用：通用方法

import io, os, sys, zipfile, platform
import hashlib
from pyqrcode import QRCode

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
def ShowQRCode(strIP, strPort, servertype, showtype):

    #生成二维码
    sInfo = strIP + ':' + strPort + '-' + str(servertype)
    img = QRCode(sInfo)
    qrStorage = io.BytesIO()
    img.png(qrStorage, scale=10)

    #二维码在命令行显示
    if showtype == 2:
        osName = platform.system()
        if osName == 'Windows':
            enableCmdQR = 1
        else:
            enableCmdQR = -2

        print_cmd_qr(img.text(1), enableCmdQR=enableCmdQR)
    #直接显示二维码
    else:
        img.show()