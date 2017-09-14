//
//  ViewController.swift
//  wifitransformclientswift
//
//  Created by PaiConor on 2017/9/13.
//  Copyright © 2017年 PaiConorMAPZONE. All rights reserved.
//

import UIKit
import AVFoundation

class ViewController: UIViewController, AVCaptureMetadataOutputObjectsDelegate {

    @IBOutlet weak var txtInfo: UITextView!
    var captureSession: AVCaptureSession?
    var videoPreviewLayer: AVCaptureVideoPreviewLayer?
    var qrCodeFrameView: UIView?
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        let captureDevice = AVCaptureDevice.default(for: .video)
        
        do {
            let input = try AVCaptureDeviceInput(device: captureDevice!)
            
            captureSession = AVCaptureSession()
            captureSession?.addInput(input as AVCaptureInput)
            let captureMetadataOutput = AVCaptureMetadataOutput()
            captureSession?.addOutput(captureMetadataOutput)
            captureMetadataOutput.setMetadataObjectsDelegate(self, queue: DispatchQueue.main)
            captureMetadataOutput.metadataObjectTypes = [.qr]
            videoPreviewLayer = AVCaptureVideoPreviewLayer(session: captureSession!)
            videoPreviewLayer?.videoGravity = AVLayerVideoGravity.resizeAspectFill
            videoPreviewLayer?.frame = view.layer.bounds
            view.layer.addSublayer(videoPreviewLayer!)
            captureSession?.startRunning()
        } catch let error as NSError {
            print(error)
        }
        
        // Initialize QR Code Frame to highlight the QR code
        qrCodeFrameView = UIView()
        qrCodeFrameView?.layer.borderColor = UIColor.green.cgColor
        qrCodeFrameView?.layer.borderWidth = 2
        view.addSubview(qrCodeFrameView!)
        view.bringSubview(toFront: qrCodeFrameView!)
    }
    
    func metadataOutput(_ output: AVCaptureMetadataOutput, didOutput metadataObjects: [AVMetadataObject], from connection: AVCaptureConnection) {
        if metadataObjects.count == 0 {
            return
        }
        
        let metadataObj = metadataObjects[0] as! AVMetadataMachineReadableCodeObject
        
        if metadataObj.type == .qr {
            
            // If the found metadata is equal to the QR code metadata then update the status label's text and set the bounds
            let barCodeObject = videoPreviewLayer?.transformedMetadataObject(for: metadataObj as AVMetadataMachineReadableCodeObject) as! AVMetadataMachineReadableCodeObject
            qrCodeFrameView?.frame = barCodeObject.bounds;
            
            if metadataObj.stringValue != nil {
                print(metadataObj.stringValue as Any)
                captureSession?.stopRunning()
                view.bringSubview(toFront: txtInfo!)
                
                //为了避免造成主线程卡顿，使用异步的方式进行无线传输
                DispatchQueue.global(qos: .userInitiated).async {
                    self.transformData(strQRCode: metadataObj.stringValue!)
                }
            }
        }
    }
    
    //在异步线程中更新主线程控件信息
    func showinfo(strInfo : String) {
        
        DispatchQueue.main.async {
            self.txtInfo.text = self.txtInfo.text + "\r\n" + strInfo
        }
    }
    
    //网络请求封装，返回值是连接是否成功和请求返回的字符串
    func request(urlstring : String) -> (bRet : Bool, sRet : String) {
        
        //url编码处理，防止特殊字符无法传输
        let encodedStr = urlstring.addingPercentEncoding(withAllowedCharacters: CharacterSet.urlQueryAllowed)
        let url:NSURL! = NSURL(string: encodedStr!)
        let urlRequest : NSURLRequest = NSURLRequest(url: url as URL, cachePolicy: .useProtocolCachePolicy, timeoutInterval: 1)
        var response:URLResponse?
        
        do{
            //发出请求
            let received:NSData? = try NSURLConnection.sendSynchronousRequest(urlRequest as URLRequest, returning: &response) as NSData
            let datastring = NSString(data:received! as Data, encoding: String.Encoding.utf8.rawValue)
            return (true, datastring! as String)
            
        } catch let error as NSError {
            print(error)
            return (false, "")
        }
    }
    
    
    //网络请求封装，下载文件到指定目录
    func downloadrequest(urlstring : String, savePath : String) -> Bool {
        
        //url编码处理，防止特殊字符无法传输
        let encodedStr = urlstring.addingPercentEncoding(withAllowedCharacters: CharacterSet.urlQueryAllowed)
        let url:NSURL! = NSURL(string: encodedStr!)
        let urlRequest : NSURLRequest = NSURLRequest(url: url as URL, cachePolicy: .useProtocolCachePolicy, timeoutInterval: 100)
        var response:URLResponse?
        
        do{
            //发出请求
            let received:NSData? = try NSURLConnection.sendSynchronousRequest(urlRequest as URLRequest, returning: &response) as NSData
            
            var urlFile = NSURL(fileURLWithPath: savePath)
            try received?.write(to: urlFile as URL, options: .atomicWrite)
            return true
            
        } catch let error as NSError {
            print(error)
            return false
        }
    }
    
    //无线传输
    func transformData(strQRCode : String) {
        
        if (strQRCode == ""){
            return
        }
        
        //显示连接字符串
        showinfo(strInfo: "\r\n已获取连接字符串：" + strQRCode)
        
        //连接字符串正确性验证
        if (!strQRCode.contains("mztransform")) {
            showinfo(strInfo: "该连接字符串非MAPZONE无线传输字符串，传输中止！")
            return
        }
        
        //解析连接字符串
        let codevalues = strQRCode.split(separator: "-")
        let conType = codevalues[0]
        let serverVersion = codevalues[1]
        let port = codevalues[2]
        let ips = codevalues[3].split(separator: ":")
        
        showinfo(strInfo: "解析连接字符串成功，正在检测可连接IP...")
        
        //测试IP连接
        var connIP : String = ""
        for i in 0...ips.count - 1 {
            let ip = ips[i]
            let (bRet, _) = request(urlstring: "http://" + ip + ":" + port + "/connectdone")
            
            if (bRet) {
                connIP = String(ip)
                showinfo(strInfo: "检测到可连接IP：" + connIP)
            }
        }
        
        if connIP == "" {
            showinfo(strInfo: "无法连接服务器！")
            return
        }
        
        //通知服务器连接成功
        let _ = request(urlstring: "http://" + connIP + ":" + port + "/showinfo?info=客户端连接成功!")
        
        //数据下载
        if conType == "mztransformdownload" {
            
            //获取下载文件信息
            let (_, sRet) = request(urlstring: "http://" + connIP + ":" + port + "/downloadfileinfo")
            showinfo(strInfo: "获取下载文件信息成功！具体信息：" + sRet)
            
            do{
                let respJsonData:NSData = sRet.data(using: String.Encoding.utf8, allowLossyConversion: false)! as NSData
                let decodedJsonDict:[String:AnyObject] = try JSONSerialization.jsonObject(with: respJsonData as Data, options: JSONSerialization.ReadingOptions.mutableContainers) as! [String:AnyObject]
                
                let _ = request(urlstring: "http://" + connIP + ":" + port + "/showinfo?info=正在下载数据...")
                showinfo(strInfo: "正在下载数据...")
                
                //清空临时目录
                let tempPath = NSHomeDirectory() + "/Documents/temp/"
                if (FileManager.default.fileExists(atPath: tempPath)){
                    try FileManager.default.removeItem(atPath: tempPath)
                }
                try FileManager.default.createDirectory(atPath: tempPath, withIntermediateDirectories: true, attributes: [:])
                
                let savefile = tempPath + (decodedJsonDict["fileid"] as! String) + ".zip"
                let downloadurlstring = "http://" + connIP + ":" + port + "/download?fileid=" + (decodedJsonDict["fileid"] as! String)
                let bret1 = downloadrequest(urlstring: downloadurlstring, savePath: savefile)
                
                if (!bret1) {
                    let _ = request(urlstring: "http://" + connIP + ":" + port + "/showinfo?info=数据下载失败！")
                    showinfo(strInfo: "数据下载失败！")
                    return
                }
                else {
                    let _ = request(urlstring: "http://" + connIP + ":" + port + "/showinfo?info=数据下载成功！")
                    showinfo(strInfo: "数据下载成功！")
                }
                
                let _ = request(urlstring: "http://" + connIP + ":" + port + "/transformdone")
                
            } catch let error as NSError {
                print(error)
            }
        }
    }
}

