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
                
                DispatchQueue.global(qos: .userInitiated).async {
                    self.transformData(strQRCode: metadataObj.stringValue!)
                }
            }
        }
    }
    
    func showinfo(strInfo : String) {
        
        DispatchQueue.main.async {
            
            self.txtInfo.text = self.txtInfo.text + "\r\n" + strInfo
        }
    }
    
    func request(urlstring : String) -> (bRet : Bool, sRet : String) {
        
        let encodedStr = urlstring.addingPercentEncoding(withAllowedCharacters: CharacterSet.urlQueryAllowed)
        let url:NSURL! = NSURL(string: encodedStr!)
        let urlRequest : NSURLRequest = NSURLRequest(url: url as URL, cachePolicy: .useProtocolCachePolicy, timeoutInterval: 1)
        
        //响应对象
        var response:URLResponse?
        do{
            //发出请求
            let received:NSData? = try NSURLConnection.sendSynchronousRequest(urlRequest as URLRequest, returning: &response) as NSData
            let datastring = NSString(data:received! as Data, encoding: String.Encoding.utf8.rawValue)
            return (true, datastring! as String)
            
        }catch _ as NSError{
            return (false, "")
        }
    }
    
    func transformData(strQRCode : String) {
        
        if (strQRCode == ""){
            return
        }
        
        //显示连接字符串
        showinfo(strInfo: "\r\n连接字符串：" + strQRCode)
        
        //解析连接字符串
        let codevalues = strQRCode.split(separator: "-")
        let conType = codevalues[0]
        let port = codevalues[1]
        let ips = codevalues[2].split(separator: ":")
        
        //测试IP连接
        var connIP : String = ""
        for i in 0...ips.count - 1 {
            let ip = ips[i]
            let (bRet, _) = request(urlstring: "http://" + ip + ":" + port + "/connectdone")
            
            if (bRet) {
                connIP = String(ip)
                showinfo(strInfo: "获得到可连接IP：" + connIP)
            }
        }
        
        if connIP == "" {
            print("无法连接")
            showinfo(strInfo: "无法连接服务器")
            return
        }
        
        //通知服务器连接成功
        let _ = request(urlstring: "http://" + connIP + ":" + port + "/showinfo?info=客户端连接成功!")
        
        //数据下载
        if conType == "mztransformdownload" {
            
            let (_, sRet) = request(urlstring: "http://" + connIP + ":" + port + "/downloadfileinfo")
            showinfo(strInfo: "获取下载文件信息：" + sRet)
        }
    }
}

