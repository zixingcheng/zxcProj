# -*- coding: utf-8 -*-
"""
Created on  张斌 2019-11-22 16:00:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    支付接口--阿里支付宝
"""

import sys
import getopt
import myData_Trans, myData_Json, myDebug, myError

from alipay import AliPay
import time, qrcode
 
 
alipay_public_key_string = '''-----BEGIN PUBLIC KEY-----
    MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCX6P+rGJsthw213ZPUtz/F0wjUTpl0LfrBXkPr2tdiskaTp8g1/kWXmIzX67Hs3VG3UvrjegzbxMnDzKuK7fPXlX//Y/wp5yXUYR0cOfxmwJAcuKVlAGg2KzEYvqRnB+69mVHmIoQL4fb//r1hDzxZk4yMO1uYgZ1kKDgAydZikQIDAQAB
-----END PUBLIC KEY-----'''
 
app_private_key_string = '''-----BEGIN RSA PRIVATE KEY-----
    MIICXAIBAAKBgQCX6P+rGJsthw213ZPUtz/F0wjUTpl0LfrBXkPr2tdiskaTp8g1/kWXmIzX67Hs3VG3UvrjegzbxMnDzKuK7fPXlX//Y/wp5yXUYR0cOfxmwJAcuKVlAGg2KzEYvqRnB+69mVHmIoQL4fb//r1hDzxZk4yMO1uYgZ1kKDgAydZikQIDAQABAoGAOPVfL8sJHDgAVwmezWpsWgN30wsplJtM40YyF3Q1wEbyGZkWg9A0TdQgMzGnxBVz91YAxlxUB+8wa98JDw2LmN0MZfo8C68ZMF4DfA8SpWuWpgCeJzS3KQq9czE+vPYwGyFnlEB8+/qYK/tv5qd4w/g1zIZXMcNcTyn9qQK4+EECQQDHDIMTHy1OK2GZsgHpfRSrk33uStQpNf8QBSZIiYoleZHkxuTl289W5iSqN5/lpf+hX0tL/mp9MkXMRUcgmPOZAkEAw1/GTCdxzux5Gb4SDBX4JDeUY/xJB/gYmnvyeZXS16ynQbWGJfblwXonv/QXCJwznmCV6aXAAira87VFEejBuQJAFvIvTg4DCAbiOniV1dfQgTMAim7f5FxQKgWd8zC/1zAbjHcNPh5H2amwQlslOLEZNf4pTPpoRkR8XV8DIxPeyQJBALYmW+1yNQQTqlAayh6keOXjP6D8fGZGo0GcX5OF4L4dhQ6ZG8nXZ5u7tMWc38CySNnW+M2OL/aVV+8xSIUK+VkCQBiQgb0VPGsxYQOK7v2CPgCUF8g+UlvW4GjlD7MpOBinX9y0ghSYAvsI53ocHWJhUy6btNbd8Q5biIhnVAZNzow=
-----END RSA PRIVATE KEY-----'''
 
#注意：一个是支付宝公钥，一个是应用私钥
APP_ID = '2016101600702013'
NOTIFY_URL = "https://your_domain/alipay_callback"
 
 
def init_alipay_cfg():
    '''
    初始化alipay配置
    :return: alipay 对象
    '''
    alipay = AliPay(
        appid=APP_ID,
        app_notify_url=NOTIFY_URL,  # 默认回调url
        app_private_key_string=app_private_key_string,
        alipay_public_key_string=alipay_public_key_string,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        sign_type="RSA",   # RSA 或者 RSA2
        debug = True       # 默认False ,若开启则使用沙盒环境的支付宝公钥
    )
    return alipay
 
 
def get_qr_code(code_url):
    '''
    生成二维码
    :return None
    '''
    #print(code_url)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=1
    )
    qr.add_data(code_url)  # 二维码所含信息
    img = qr.make_image()  # 生成二维码图片
    img.save(r'C:\Users\SEEMORE\Desktop\qr_test_ali.png')
    print('二维码保存成功！')
 
 
def preCreateOrder(subject:'order_desc' , out_trade_no:int, total_amount:(float,'eg:0.01')):
    '''
    创建预付订单
    :return None：表示预付订单创建失败  [或]  code_url：二维码url
    '''
    result = init_alipay_cfg().api_alipay_trade_precreate(
        subject=subject,
        out_trade_no=out_trade_no,
        total_amount=total_amount)
    print('返回值：',result)
    code_url = result.get('qr_code')
    if not code_url:
        print(result.get('预付订单创建失败：','msg'))
        return
    else:
        get_qr_code(code_url)
        #return code_url
 
 
def query_order(out_trade_no:int, cancel_time:int and 'secs'):
    '''
    :param out_trade_no: 商户订单号
    :return: None
    '''
    print('预付订单已创建,请在%s秒内扫码支付,过期订单将被取消！'% cancel_time)
    # check order status
    _time = 0
    for i in range(10):
        # check every 3s, and 10 times in all
 
        print("now sleep 2s")
        time.sleep(2)
 
        result = init_alipay_cfg().api_alipay_trade_query(out_trade_no=out_trade_no)
        if result.get("trade_status", "") == "TRADE_SUCCESS":
            print('订单已支付!')
            print('订单查询返回值：',result)
            break
 
        _time += 2
        if _time >= cancel_time:
            cancel_order(out_trade_no,cancel_time)
            return
 
 
def cancel_order(out_trade_no:int, cancel_time=None):
    '''
    撤销订单
    :param out_trade_no:
    :param cancel_time: 撤销前的等待时间(若未支付)，撤销后在商家中心-交易下的交易状态显示为"关闭"
    :return:
    '''
    result = init_alipay_cfg().api_alipay_trade_cancel(out_trade_no=out_trade_no)
    #print('取消订单返回值：', result)
    resp_state = result.get('msg')
    action = result.get('action')
    if resp_state=='Success':
        if action=='close':
            if cancel_time:
                print("%s秒内未支付订单，订单已被取消！" % cancel_time)
        elif action=='refund':
            print('该笔交易目前状态为：',action)
 
        return action
 
    else:
        print('请求失败：',resp_state)
        return
 
 
def need_refund(out_trade_no:str or int, refund_amount:int or float, out_request_no:str):
    '''
    退款操作
    :param out_trade_no: 商户订单号
    :param refund_amount: 退款金额，小于等于订单金额
    :param out_request_no: 商户自定义参数，用来标识该次退款请求的唯一性,可使用 out_trade_no_退款金额*100 的构造方式
    :return:
    '''
    result = init_alipay_cfg().api_alipay_trade_refund(out_trade_no=out_trade_no,
                                                       refund_amount=refund_amount,
                                                       out_request_no=out_request_no)
 
    if result["code"] == "10000":
        return result  #接口调用成功则返回result
    else:
        return result["msg"] #接口调用失败则返回原因
 
 
def refund_query(out_request_no:str, out_trade_no:str or int):
    '''
    退款查询：同一笔交易可能有多次退款操作（每次退一部分）
    :param out_request_no: 商户自定义的单次退款请求标识符
    :param out_trade_no: 商户订单号
    :return:
    '''
    result = init_alipay_cfg().api_alipay_trade_fastpay_refund_query(out_request_no, out_trade_no=out_trade_no)
 
    if result["code"] == "10000":
        return result  #接口调用成功则返回result
    else:
        return result["msg"] #接口调用失败则返回原因
 
 
if __name__ == '__main__':
    #cancel_order(1527212120)
    subject = "话费余额充值"
    out_trade_no =int(time.time())
    total_amount = 0.01
    preCreateOrder(subject,out_trade_no,total_amount)
 
    query_order(out_trade_no,40)
 
    print('5s后订单自动退款')
    time.sleep(5)
    print(need_refund(out_trade_no,0.01,111))
 
    print('5s后查询退款')
    time.sleep(5)
    print(refund_query(out_request_no=111, out_trade_no=out_trade_no))

    #操作完登录 https://authsu18.alipay.com/login/index.htm中的对账中心查看是否有一笔交易生成并退款