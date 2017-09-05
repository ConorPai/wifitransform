# coding=utf-8
# 作用：通用方法

import os, zipfile
import hashlib

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