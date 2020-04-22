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

class Testpayamountdatacommit(unittest.TestCase):


    @classmethod    #声明为类方法
    def setUpClass(cls):  #类方法，注意后面的参数是cls
        logging.debug('>>>>>setUpClass,测试类Testpayamountdatacommit开始测试>>>>>')
        #实例化excel类
        cls.excel = Excel("testcase.xls")
        #类执行前，获取payamountdatacommit这个sheet里的数据
        cls.excel.excel_replace("payamountdatacommit","data","newbillid","oldbillid")
        cls.excel1 = Excel("testcase.xls")
        cls.data_list = cls.excel1.get_sheet_list("payamountdatacommit")

    @classmethod
    def tearDownClass(cls):
        logging.debug('<<<<<tearDownClass,测试类Testpayamountdatacommit3测试结束<<<<<')

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def dbassert(self,billid,data,res_result):
        #数据库实例化
        db = DB()
        #数据库断言
        #主表断言
        payamountjson = eval(data['payamountjson'])

        data_result_exterbill = db.query("select e.billstatus,e.paystatus from t_exterbill e where billid ='{billid}'".format(billid=billid))
        logging.info(data_result_exterbill)
        for i in range(len(data_result_exterbill)): 
            self.assertEqual(data_result_exterbill[i][0],1,msg="单据状态")
            self.assertEqual(data_result_exterbill[i][1],'1',msg="收款状态")
        
        #t_payamount断言
        data_result_payamount = db.query("select p.billtype,p.billid,p.paytype,p.payamount,p.remark from t_payamount p where billid ='{billid}' order by p.payamount desc".format(billid=billid))
        logging.info(data_result_payamount)

        for j in range(len(data_result_payamount)): 
            self.assertEqual(data_result_payamount[j][0],521,msg="单据状态")
            self.assertEqual(data_result_payamount[j][1],res_result['data'],msg="单据号")  
            self.assertEqual(data_result_payamount[j][2],payamountjson[j]['paytype'],msg="收款类型")       
            self.assertEqual(data_result_payamount[j][3],payamountjson[j]['payamount'],msg="收款金额")       
            self.assertEqual(data_result_payamount[j][4],payamountjson[j]['remark'],msg="备注")       

        #t_payamountdetail断言
        data_result_payamountdetail = db.query("select p.billtype,p.billid,p.paytype,p.payamount,p.remark from t_payamount p where billid ='{billid}' order by p.payamount desc".format(billid=billid))
        logging.info(data_result_payamountdetail)
        for k in range(len(data_result_payamountdetail)): 
            self.assertEqual(data_result_payamountdetail[k][0],521,msg="单据状态")
            self.assertEqual(data_result_payamountdetail[k][1],res_result['data'],msg="单据号")  
            self.assertEqual(data_result_payamountdetail[k][2],payamountjson[k]['paytype'],msg="收款类型")       
            self.assertEqual(data_result_payamountdetail[k][3],payamountjson[k]['payamount'],msg="收款金额")       
            self.assertEqual(data_result_payamountdetail[k][4],payamountjson[k]['remark'],msg="备注")

        #t_payralation断言
        data_result_t_payralation = db.query("select * from t_payralation where billid ='{billid}' ".format(billid=billid))
        logging.info(data_result_t_payralation)   
        self.assertIsNotNone(data_result_t_payralation,msg="非空")

        return  logging.info('》》》》》》》》》》》》》》》》》》》》》》》》》》》》》断言完成》》》》》》》》》》》》》》》》》》》》》》》》》》》》》')

    def payamountdatacommit(self,casename):
        case_data = self.excel.get_test_case(self.data_list,casename)
        case_name = case_data.get('case_name')
        url = case_data.get('url')
        data = eval(case_data.get('data'))
        billid = data.get('billid')
        #发送请求
        res = requests.get(url=url,params=data)
        #返回结果，并将json转字符串
        res_dict = json.dumps(res.json(),indent=2,ensure_ascii=False,sort_keys=True)
        #写入日志
        log_case_info(case_name , url , data , res_dict)
        #断言返回码
        self.assertEqual(res.json()['code'],'200',msg='返回码不等于200，OK')
        #断言
        res_result = res.json()
        self.dbassert(billid,data,res_result)

    def test_01_payamountdatacommit(self):   
        self.payamountdatacommit("case01")    

    def test_02_payamountdatacommit(self):
        self.payamountdatacommit("case02")
    
    def test_03_payamountdatacommit(self):
        self.payamountdatacommit("case03")

    def test_04_payamountdatacommit(self):
        self.payamountdatacommit("case04")

    def test_05_payamountdatacommit(self):
        self.payamountdatacommit("case05")



if __name__=='__main__':   # 如果是直接从当前模块执行（非别的模块调用本模块）
    unittest.main(verbosity=2)    # 运行本测试类所有用例,verbosity为结果显示级别