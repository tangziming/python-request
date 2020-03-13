import unittest
import requests
import json
from db import *
from read_excel import Excel
import logging

def setUpModule():   #当前模块执行前执行一次
    print('=====setUpModule,'+__name__+'模块开始测试=====')


def tearDownModule():  #当前模块执行后执行一次
    print('=====tearDownModule,'+__name__+'模块测试结束=====')



class TestSaveDataV3(unittest.TestCase):
    #url = 'http://192.168.0.190/appapi/rest/exterbillv2/saveDataV3'
    

    

    @classmethod           #声明为类方法
    def setUpClass(cls):   #类方法，注意后面是cls
        print('=====setUpClass,测试类TestSaveData3开始测试======')
        cls.excel =  Excel("testcase.xls")
        cls.data_list = cls.excel.get_sheet_list("TestSaveDataV3")       
        cls.content = []


    @classmethod
    def tearDownClass(cls):
        print('=====setUpClass,测试类TestSaveData3测试结束======')
        print(cls.content)
        print(">"*20)
        cls.excel.excel_write("PayamountDataCommit","newbillid",cls.content)

    def setUp(self):
        pass


    def tearDown(self):
        pass

    #数据库断言方法
    def dbassert(self,billid,shopcode,shopbacktype,trademodecode,yys='N'):
        #数据库实例化
        db = DB()
        #数据库断言
        #主表断言
        exterbill_result = db.query("select a.billtype 单据类型,a.billid 单据号 ,a.billstatus 单据状态,a.shopcode 门店,a.shopbacktype 销售类型,a.trademodecode 业务类型 ,a.paystatus 收款状态,a.operator 制单人,a.operatetime 单据日期  from t_exterbill a  where a.billid ='{}'".format(billid))
        #print(exterbill_result)
        for i in range(len(exterbill_result)):
            self.assertEqual(exterbill_result[i][0],110,msg="单据类型是否110")
            self.assertEqual(exterbill_result[i][1],billid,msg="单据号是否相等")
            self.assertEqual(exterbill_result[i][2],0,msg="单据状态是否0") 
            self.assertEqual(exterbill_result[i][3],shopcode,msg="门店是否正确")
            self.assertEqual(exterbill_result[i][4],shopbacktype,msg="销售类型是否000")
            self.assertEqual(exterbill_result[i][5],trademodecode,msg="业务类型是否01")
            self.assertEqual(exterbill_result[i][6],'0',msg="收款状态是否0")
            self.assertIsNotNone(exterbill_result[i][7],msg="单据日期不为空")

        #明细表断言                                          
        exterbilldetail_result = db.query("select  b.billtype 单据类型,b.billid 单据号 ,b.storeshopcode 出库门店, b.storecode 仓库, b.goodscode 商品编码,b.exchangerate 定价, b.priceincludetax 单价,b.realnumber 数量 ,b.realsum 销售金额,b.lowestprice 最低销售价, b.costprice 成本, b.coachprice 考核低价,b.goodsid 串号  from t_exterbilldetail b where b.billid ='{}'".format(billid))
        #print(exterbilldetail_result)
        for x in range(len(exterbilldetail_result)):
            self.assertEqual(exterbilldetail_result[x][0],110,msg="单据类型是否110")
            self.assertEqual(exterbilldetail_result[x][1],billid,msg="单据号是否相等")
            self.assertIsNotNone(exterbilldetail_result[x][4],msg="商品编码非空")
            self.assertIsNotNone(exterbilldetail_result[x][5],msg="定价非空")
            self.assertIsNotNone(exterbilldetail_result[x][6],msg="单价非空")
            self.assertIsNotNone(exterbilldetail_result[x][7],msg="数量非空")    
            self.assertIsNotNone(exterbilldetail_result[x][8],msg="销售金额非空")            
            self.assertIsNotNone(exterbilldetail_result[x][9],msg="最低销售价非空")            

        #运营商断言
        if  yys == 'Y':
            paydetail_result = db.query("select t.serial,t.billtype,t.billid,t.paytype,t.goodscode,t.money,t.serviceid,t.businessnumber,t.businesstype,t.effect,t.yyssitecode,t.yyspaytype,t.prepayment,t.actualprepayment,t.ruleid from t_paydetails t where t.billid ='{}'".format(billid))
            for a in  range(len(paydetail_result)):
                self.assertEqual(paydetail_result[a][1],110,msg="单据类型是否110")
                self.assertEqual(paydetail_result[a][2],billid,msg="单据号是否相等")
                self.assertEqual(paydetail_result[a][3],"YYS",msg="运营商写死YYS")
                for b in range(len(paydetail_result[a])):
                    self.assertIsNotNone(paydetail_result[a][b],msg="不允许有空值")
                    
        return  print('断言完成')

    #常规业务   （串号+配件， 代金券，优惠券）
    def test_01__saveDateV3(self):

        case_data = self.excel.get_test_case(self.data_list,"savedate_normal")
        url = case_data.get('url')
        data = eval(case_data.get('data')) 
        res = requests.post(url=url,data=data)
        
        #res_dict = json.dumps(res.json(),indent=2,ensure_ascii=False,sort_keys=True)
        #print(res_dict)


        #获取响应体的数据（单据号，门店名称,业务类型,销售类型）
        billid = res.json()['data']['exterBill']['billid']   
        shopcode = res.json()['data']['exterBill']['shopcode']
        shopbacktype = json.loads(data['exterbilljson'])['shopbacktype']
        trademodecode = json.loads(data['exterbilljson'])['trademodecode']


        #返回值断言
        self.assertEqual(res.json()['code'],'200',msg='返回码不等于200')

        #数据库断言
        self.dbassert(billid,shopcode,shopbacktype,trademodecode)
        self.content.append(billid)
 
    
    #运营商业务 （套餐+白卡）
    def test_02__saveDateV3(self):

        case_data = self.excel.get_test_case(self.data_list,"savedate_yys")
        url = case_data.get('url')
        data = eval(case_data.get('data')) 
        res = requests.post(url=url,data=data)

        #res_dict = json.dumps(res.json(),indent=2,ensure_ascii=False,sort_keys=True)
        #print(res_dict)

        #获取响应体的数据（单据号，门店名称）
        billid = res.json()['data']['exterBill']['billid']
        shopcode = res.json()['data']['exterBill']['shopcode']
        shopbacktype = json.loads(data['exterbilljson'])['shopbacktype'] 
        trademodecode = json.loads(data['exterbilljson'])['trademodecode']


        #返回值断言
        self.assertEqual(res.json()['code'],'200',msg='返回码不等于200')

        #数据库断言
        self.dbassert(billid,shopcode,shopbacktype,trademodecode,yys='Y')
        self.content.append(billid)


    #虚库业务 （虚库商品）   
    def test_03__saveDateV3(self):

        case_data = self.excel.get_test_case(self.data_list,"savedate_virtual")
        url = case_data.get('url')
        data = eval(case_data.get('data')) 
        res = requests.post(url=url,data=data)

        #res_dict = json.dumps(res.json(),indent=2,ensure_ascii=False,sort_keys=True)
        #print(res_dict)


        #获取响应体的数据（单据号，门店名称,业务类型,销售类型）
        billid = res.json()['data']['exterBill']['billid']    
        shopcode = res.json()['data']['exterBill']['shopcode']
        shopbacktype = json.loads(data['exterbilljson'])['shopbacktype']
        trademodecode = json.loads(data['exterbilljson'])['trademodecode']


        #返回值断言
        self.assertEqual(res.json()['code'],'200',msg='返回码不等于200')

        #数据库断言
        self.dbassert(billid,shopcode,shopbacktype,trademodecode)
        self.content.append(billid)
      
    




if __name__=='__main__':   # 如果是直接从当前模块执行（非别的模块调用本模块）
    unittest.main(verbosity=2)    # 运行本测试类所有用例,verbosity为结果显示级别