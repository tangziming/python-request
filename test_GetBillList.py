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

class TestGetBillList(unittest.TestCase):


    @classmethod    #声明为类方法
    def setUpClass(cls):  #类方法，注意后面的参数是cls
        logging.debug('>>>>>setUpClass,测试类TestGetBillList开始测试>>>>>')
        #实例化excel类
        cls.excel = Excel("testcase.xls")
        #类执行前，获取GetBillList这个sheet里的数据
        cls.data_list = cls.excel.get_sheet_list("GetBillList")
    
    @classmethod
    def tearDownClass(cls):
        logging.debug('<<<<<tearDownClass,测试类TestGetBillList测试结束<<<<<')
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def dbassert(self,shopcode,rownum,billtype,res_result):
        #数据库实例化
        db = DB()
        #数据库断言
        #主表断言
        data_result = db.query('''select *
                                        from (select a.billtype,
                                                    a.billid,
                                                    a.shopcode,
                                                    a.billstatus,
                                                    a.operator,
                                                    a.handleman,
                                                    a.gatherman,
                                                    a.earnestmoney,
                                                    a.remark,
                                                    a.baucode,
                                                    a.shopbacktype,
                                                    a.reviewman,
                                                    a.approveman,
                                                    a.gatherway,
                                                    a.vipinfoid,
                                                    a.paystatus,
                                                    v.cardlevel,
                                                    o.dataname
                                                from t_exterbill a,t_crm_vipinfo v,t_otherbasedata o
                                                where a.shopcode = '{shopcode}'
                                                and billtype = '{billtype}'
                                                and v.vipinfoid=a.vipinfoid
                                                and o.nodecode='CARDLEVEL'
                                                and o.datacode=v.cardlevel
                                                order by billid desc)
                                        where rownum <={rownum}
                                '''.format(shopcode=shopcode,rownum=rownum,billtype=billtype))
        logging.info(data_result)
        for j in range(len(data_result)):
            self.assertEqual(data_result[j][0],res_result['data'][j]['BILLTYPE'],msg="BILLTYPE")
            self.assertEqual(data_result[j][1],res_result['data'][j]['BILLID'],msg="billid")
            self.assertEqual(data_result[j][2],res_result['data'][j]['SHOPCODE'],msg="SHOPCODE")
            self.assertEqual(data_result[j][3],res_result['data'][j]['BILLSTATUS'],msg="BILLSTATUS")
            self.assertEqual(data_result[j][4],res_result['data'][j]['OPERATOR'],msg="OPERATOR")
            self.assertEqual(data_result[j][5],res_result['data'][j]['HANDLEMAN'],msg="HANDLEMAN")
            
        return  logging.info('》》》》》》》》》》》》》》》》》》》》》》》》》》》》》断言完成》》》》》》》》》》》》》》》》》》》》》》》》》》》》》')

    def GetBillList(self,casename):
        case_data = self.excel.get_test_case(self.data_list,casename)
        case_name = case_data.get('case_name')
        url = case_data.get('url')
        data = eval(case_data.get('data'))
        shopcode = data.get('shopcode')
        rownum = data.get('rows')
        billtype = data.get('billtype')
        #发送请求
        res = requests.get(url=url,params=data)
        #返回结果，并将json转字符串
        res_dict = json.dumps(res.json(),indent=2,ensure_ascii=False,sort_keys=True)
        #写入日志
        log_case_info(case_name , url , data , res_dict)
        #断言返回码
        self.assertEqual(res.json()['code'],'200',msg=logging.error('返回码不等于200，OK'))
        #断言
        res_result = res.json()
        self.dbassert(shopcode,rownum,billtype,res_result)

    def test_01_GetBillList(self):   
        self.GetBillList("case01")

    def test_02_GetBillList(self):
        self.GetBillList("case02")
    
    def test_03_GetBillList(self):
        self.GetBillList("case03")

    def test_04_GetBillList(self):
        self.GetBillList("case04")





if __name__=='__main__':   # 如果是直接从当前模块执行（非别的模块调用本模块）
    unittest.main(verbosity=2)    # 运行本测试类所有用例,verbosity为结果显示级别