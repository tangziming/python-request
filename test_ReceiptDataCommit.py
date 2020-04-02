import unittest
from db import *
from read_excel import *
import json
import requests
from log import *

def setUpModule(): #当前模块执行前执行一次
    logging.debug('>>>>>setUpModule,'+__name__+'模块开始测试>>>>>')

def tearDownModule():  #当前模块执行后执行一次
    logging.debug('<<<<<tearDownModule,'+__name__+'模块测试结束<<<<<')

class TestReceiptDataCommit(unittest.TestCase):


    @classmethod    #声明为类方法
    def setUpClass(cls):  #类方法，注意后面的参数是cls
        logging.debug('>>>>>setUpClass,测试类TestReceiptDataCommit开始测试>>>>>')
        #实例化excel类
        cls.excel = Excel("testcase.xls")
        #类执行前，获取ReceiptDataCommit这个sheet里的数据
        cls.data_list = cls.excel.get_sheet_list("ReceiptDataCommit")
        cls.newbillid =[]
    
    @classmethod
    def tearDownClass(cls):
        logging.debug('<<<<<tearDownClass,测试类TestReceiptDataCommit3测试结束<<<<<')
        cls.excel.excel_write("savePayamount","newbillid",cls.newbillid)
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def dbassert(self,billid,data):
        #数据库实例化
        db = DB()
        #数据库断言
        #主表断言
        exterbilljson = eval(data['exterbilljson'])
        
        data_result = db.query("select a.billtype,a.billid,a.shopcode,a.billstatus,a.handleman, to_char(a.earnestmoney),a.remark,a.shopbacktype,a.reviewman,a.approveman,a.gatherway,a.vipinfoid from t_exterbill a   where billid ='{}'".format(billid))
        logging.info(data_result)
        for j in range(len(data_result)):  
            self.assertEqual(data_result[j][0],521,msg="单据类型")
            self.assertEqual(data_result[j][1],billid,msg="单据ID")
            self.assertEqual(data_result[j][2],exterbilljson['SHOPCODE'],msg="门店ID")
            self.assertEqual(data_result[j][3],0,msg="单据状态")
            self.assertEqual(data_result[j][4],exterbilljson['HANDLEMAN'],msg="处理人")
            self.assertEqual(data_result[j][5],exterbilljson['EARNESTMONEY'],msg="金额")
            self.assertEqual(data_result[j][6],exterbilljson['REMARK'],msg="备注")
            self.assertEqual(data_result[j][7],exterbilljson['shopbacktype'],msg="销售类型")
            self.assertEqual(data_result[j][8],exterbilljson['REVIEWMAN'],msg="会员名称")
            self.assertEqual(data_result[j][9],exterbilljson['APPROVEMAN'],msg="会员电话")
            self.assertEqual(data_result[j][10],exterbilljson['GATHERWAY'],msg="支付方式")
            self.assertEqual(data_result[j][11],exterbilljson['VIPINFOID'],msg="会员ID")
            logging.info('》》》》》》》》》》》》》》》》》》》》》》》》》》》》》主表断言完成》》》》》》》》》》》》》》》》》》》》》》》》》》》》》')
        if(data['exterbilldetailjson']):
            exterbilldetailjson = eval(data['exterbilldetailjson'])
            detaildata_result = db.query("select d.billtype,d.billid,d.goodscode,to_char(d.priceincludetax),to_char(d.num),to_char(d.exchangerate),to_char(d.numberincludetax),d.goodsitem from t_exterbilldetail d where billid ='{}'".format(billid))
            logging.info(detaildata_result)
            for i in range(len(data_result)):  
                self.assertEqual(detaildata_result[i][0],521,msg="单据类型")
                self.assertEqual(detaildata_result[i][1],billid,msg="单据ID")
                self.assertEqual(detaildata_result[i][2],exterbilldetailjson[i]['GOODSCODE'],msg="门店ID")
                self.assertEqual(detaildata_result[i][3],exterbilldetailjson[i]['PRICEINCLUDETAX'],msg="单据状态")
                self.assertEqual(detaildata_result[i][4],exterbilldetailjson[i]['NUM'],msg="处理人")
                self.assertEqual(detaildata_result[i][5],exterbilldetailjson[i]['EXCHANGERATE'],msg="金额")
                self.assertEqual(detaildata_result[i][6],exterbilldetailjson[i]['NUMBERINCLUDETAX'],msg="备注")
                self.assertEqual(detaildata_result[i][7],exterbilldetailjson[i]['GOODSITEM'],msg="销售类型")
                logging.info('》》》》》》》》》》》》》》》》》》》》》》》》》》》》》明细表断言完成》》》》》》》》》》》》》》》》》》》》》》》》》》》》》')
        return  logging.info('》》》》》》》》》》》》》》》》》》》》》》》》》》》》》断言完成》》》》》》》》》》》》》》》》》》》》》》》》》》》》》')

    def ReceiptDataCommit(self,casename):
        case_data = self.excel.get_test_case(self.data_list,casename)
        case_name = case_data.get('case_name')
        url = case_data.get('url')
        data = eval(case_data.get('data'))
        
        #发送请求
        res = requests.get(url=url,params=data)
        #返回结果，并将json转字符串
        res_dict = json.dumps(res.json(),indent=2,ensure_ascii=False,sort_keys=True)
        #写入日志
        log_case_info(case_name , url , data , res_dict)
        #断言返回码
        self.assertEqual(res.json()['code'],'200',msg='返回码不等于200，OK')
        #断言
        billid = res.json()['data']['billid']
        self.newbillid.append(billid)
        if(res.json()['code']=='200'):  
            self.dbassert(billid,data)


    def test_01_ReceiptDataCommit(self):   
        self.ReceiptDataCommit("case01")    

    def test_02_ReceiptDataCommit(self):
        self.ReceiptDataCommit("case02")
    
    def test_03_ReceiptDataCommit(self):
        self.ReceiptDataCommit("case03")

    def test_04_ReceiptDataCommit(self):
        self.ReceiptDataCommit("case04")

    def test_05_ReceiptDataCommit(self):
        self.ReceiptDataCommit("case05")



if __name__=='__main__':   # 如果是直接从当前模块执行（非别的模块调用本模块）
    unittest.main(verbosity=2)    # 运行本测试类所有用例,verbosity为结果显示级别