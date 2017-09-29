# coding=utf-8
# 作用：发布微服务，提供生成二维码扫码连接下载文件功能

import os, sys, uuid, json, time, urllib.parse
from flask import Flask, request, send_from_directory, abort
from common import ShowQRCode, zip_dir, getmd5, ShowLog

app = Flask(__name__)

#临时目录
tempdir = 'aaa'

#服务API，获取下载文件信息
@app.route('/downloadfileinfo', methods=['GET'])
def download_file_info():

    global tempdir
    for parent, dirnames, filenames in os.walk(tempdir):
        for filename in filenames:
            totalfilename = tempdir + '/' + filename
            if (filename.split('.')[1] == 'zip'):
                fileinfo = {}
                fileinfo['fileid'] = filename.split('.')[0]
                fileinfo['filesize'] = os.path.getsize(totalfilename)
                fileinfo['filemd5'] = getmd5(totalfilename)

                jsonfileinfo = json.dumps(fileinfo, ensure_ascii=False)

                jsonfileinfo = jsonfileinfo.replace('\\\\', '/');
                jsonfileinfo = jsonfileinfo.replace('\\', '/');

                return jsonfileinfo, 200

    abort(404)

#服务API，下载数据
@app.route('/download', methods=['GET'])
def download_file():
    fileid = request.args.get('fileid')
    global tempdir
    filename = tempdir + '/' + fileid + '.zip'
    if os.path.isfile(filename):
        return send_from_directory(tempdir, fileid + '.zip', as_attachment=True)
    abort(404)

#服务API，上传数据
@app.route('/upload', methods=['POST'])
def upload_file():

    file = request.files['file']
    global tempdir
    filename = tempdir + '/upload.zip'
    file.save(filename)

    return 'success', 200

#服务API，客户端连接成功
@app.route('/connectdone', methods=['GET'])
def connect_done():
    global tempdir
    ShowLog(tempdir, "mzcommand:|:connectdone")
    return 'success', 200

#服务API，数据传输完成，可以关闭服务
@app.route('/transformdone', methods=['GET'])
def transformdone():
    global tempdir
    ShowLog(tempdir, "mzcommand:|:transformdone")
    return 'success', 200

#服务API，客户端提示信息
@app.route('/showinfo', methods=['GET'])
def show_info():
    info = request.args.get('info')
    infodecode = urllib.parse.unquote(info)

    global tempdir
    ShowLog(tempdir, infodecode)
    return 'success', 200

#主函数
def main():

    #获取命令行参数
    #参数1：服务类型：mztransformdownload-下载服务；mztransformupload-上传服务
    #参数2：下发数据路径或上传数据存放路径
    #参数3：IP
    #参数4：端口号
    #参数5：指定临时目录路径
    params = sys.argv

    #time.sleep(20)

    #调试补全参数
    '''
    bIsDownload = True

    if bIsDownload:
        if (len(params) == 1):
            params.append('mztransformdownload')
            params.append('/Users/paiconor/Downloads/数据下发')
            params.append('127.0.0.1:192.168.1.243:192.168.1.40:192.168.1.161:192.168.99.144')
            params.append('8098')
            params.append('temp')
        #参数只传传输目录，补全其它参数
        elif len(params) == 2:
            params.insert(1, 'mztransformdownload')
            params.append('127.0.0.1')
            params.append('8098')
            params.append('temp')
        elif len(params) == 5:
            params.append('temp')
    else:
        if (len(params) == 1):
            params.append('mztransformupload')
            params.append('/Users/paiconor/Downloads/数据下发')
            params.append('127.0.0.1')
            params.append('8098')
            params.append('temp')
        #参数只传传输目录，补全其它参数
        elif len(params) == 2:
            params.insert(1, 'mztransformupload')
            params.append('127.0.0.1')
            params.append('8098')
            params.append('temp')
        elif len(params) == 5:
            params.append('temp')

        params[5] = params[2];
    '''

    if (len(params) <= 5):
        return

    #清理临时目录
    global tempdir
    tempdir = params[5]
    if os.path.exists(tempdir):
        __import__('shutil').rmtree(tempdir)
    os.mkdir(tempdir)

    #下发数据时，将需要下发的目录压缩
    if (params[1] == 'mztransformdownload'):
        ShowLog(tempdir, '正在压缩下载数据...')
        zipfile = tempdir + '/' + str(uuid.uuid1()) +'.zip'
        zip_dir(params[2], zipfile)
        params[2] = zipfile
    
    #生成连接二维码
    ShowLog(tempdir, '正在生成二维码...')
    ShowQRCode(params[3], params[4], params[1], tempdir)

    #启动服务
    ShowLog(tempdir, '等待客户端扫描二维码...')
    app.run(host='0.0.0.0', port=int(params[4]), threaded=True)

main()
