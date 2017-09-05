# coding=utf-8
# 作用：发布微服务，提供生成二维码扫码连接下载文件功能

import os, sys, uuid
from flask import Flask, request, send_from_directory, abort
from common import GeneralQRCode, showImage, zip_dir

app = Flask(__name__)

#临时目录
tempdir = 'temp'

#服务API，连接成功
@app.route('/connectsuccess', methods=['GET'])
def connect_success():
    print '客户端连接成功'
    return 'success', 200

#服务API，下载数据
@app.route('/download', methods=['GET'])
def download_file():
    fileid = request.args.get('fileid')
    filename = 'temp/' + fileid + '.zip'
    if os.path.isfile(filename):
        return send_from_directory('temp', fileid + '.zip', as_attachment=True)
    abort(404)

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
    print '清理临时目录...'
    if os.path.exists(tempdir):
        __import__('shutil').rmtree(tempdir)
    os.mkdir(tempdir)

    #下发数据时，将需要下发的目录压缩
    if (params[1] == '1'):
        print '正在压缩上传文件...'
        zipfile = tempdir + '/' + str(uuid.uuid1()) +'.zip'
        zip_dir(params[2], zipfile)
        params[2] = zipfile
    
    #生成连接二维码
    print '正在生成二维码...'
    qrfile = tempdir + '/' + str(uuid.uuid1()) +'.jpg'
    connectString = GeneralQRCode(qrfile, int(params[1]), params[2], params[3], params[4])
    fConnString = open(tempdir + '/connectString.txt', 'a')
    fConnString.write(connectString)
    fConnString.flush()
    fConnString.close()

    showImage(qrfile)

    #启动服务
    print '启动服务...'
    app.run(host=params[3], port=int(params[4]))

main()