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

class TestGetBillDetails(unittest.TestCase):


    @classmethod    #声明为类方法
    def setUpClass(cls):  #类方法，注意后面的参数是cls
        logging.debug('>>>>>setUpClass,测试类TestGetBillDetails开始测试>>>>>')
        #实例化excel类
        cls.excel = Excel("testcase.xls")
        #类执行前，获取GetBillDetails这个sheet里的数据
        cls.data_list = cls.excel.get_sheet_list("GetBillDetails")
    
    @classmethod
    def tearDownClass(cls):
        logging.debug('<<<<<tearDownClass,测试类TestGetBillDetails测试结束<<<<<')
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def dbassert(self,shopcode,res_result):
        #数据库实例化
        db = DB()
        #数据库断言
        #主表断言
        data_result = db.query("select datacode,dataname from t_otherbasedata  where basetype  ='CompStore'and  canedit ='Y' and cansale='N' and datacode in (select storecode from t_shopstore where shopcode ='{}')".format(shopcode))
        logging.info(data_result)
        for j in range(len(data_result)):
            logging.info(data_result[j][0])
            logging.info(res_result['data'][j]['storecode'])
            logging.info(data_result[j][1])
            logging.info(res_result['data'][j]['storename'])
            self.assertEqual(data_result[j][0],res_result['data'][j]['storecode'],msg="仓库编码不相等")
            self.assertEqual(data_result[j][1],res_result['data'][j]['storename'],msg="仓库名称不相等")
            
        return  logging.info('》》》》》》》》》》》》》》》》》》》》》》》》》》》》》断言完成》》》》》》》》》》》》》》》》》》》》》》》》》》》》》')

    def GetBillDetails(self,casename):
        case_data = self.excel.get_test_case(self.data_list,casename)
        case_name = case_data.get('case_name')
        url = case_data.get('url')
        data = eval(case_data.get('data'))
        shopcode = data.get('shopcode')
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
        #self.dbassert(shopcode,res_result)

    def test_01_GetBillDetails(self):   
        self.GetBillDetails("case01")

    def test_02_GetBillDetails(self):
        self.GetBillDetails("case02")
    
    def test_03_GetBillDetails(self):
        self.GetBillDetails("case03")

    def test_04_GetBillDetails(self):
        self.GetBillDetails("case04")

    def test_05_GetBillDetails(self):
        self.GetBillDetails("case05")




if __name__=='__main__':   # 如果是直接从当前模块执行（非别的模块调用本模块）
    unittest.main(verbosity=2)    # 运行本测试类所有用例,verbosity为结果显示级别