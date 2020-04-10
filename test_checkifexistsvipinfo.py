import unittest
from db import *
from read_excel import *
import json
import requests
from log import *
import random

def setUpModule(): #当前模块执行前执行一次
    logging.debug('>>>>>setUpModule,'+__name__+'模块开始测试>>>>>')

def tearDownModule():  #当前模块执行后执行一次
    logging.debug('<<<<<tearDownModule,'+__name__+'模块测试结束<<<<<')

class Testcheckifexistsvipinfo(unittest.TestCase):


    @classmethod    #声明为类方法
    def setUpClass(cls):  #类方法，注意后面的参数是cls
        logging.debug('>>>>>setUpClass,测试类Testcheckifexistsvipinfo开始测试>>>>>')
        #实例化excel类
        cls.excel = Excel("testcase.xls")
        #类执行前，获取checkifexistsvipinfo这个sheet里的数据
        cls.data_list = cls.excel.get_sheet_list("checkifexistsvipinfo")
    
    @classmethod
    def tearDownClass(cls):
        logging.debug('<<<<<tearDownClass,测试类Testcheckifexistsvipinfo3测试结束<<<<<')
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def dbassert(self,code,res_result,data):
        #数据库实例化
        db = DB()
        #数据库断言
        #主表断言
        sql = '''select v.cardid,
                v.vipinfoid,
                v.vipname,
                v.sex,
                v.mobiletel,
                v.remark,
                v.putoutmode,
                v.shopcode,
                v.operator,
                v.cardlevel,
                v.status,
                v.flymail,
                v.integral,
                v.totalintegral,
                v.vipcardtype,
                v.vipid
            from t_crm_vipinfo v
            where mobiletel = '{mobiletel}' or vipinfoid ='{vipinfoid}'
        '''
        if (data['mobiletel']):
            mobiletel = data['mobiletel']
            vipinfoid = 123123123123123123123
        elif (data['vipinfoid']):
            mobiletel = 123123123123123123123
            vipinfoid = data['vipinfoid']        
        if code =='200' :

            data_result = db.query(sql.format(mobiletel=mobiletel,vipinfoid=vipinfoid))
            logging.info(data_result)
            for j in range(len(data_result)):
                self.assertEqual(data_result[j][0],res_result['data']['data']['CARDID'],msg="cardid不相等")
                self.assertEqual(data_result[j][1],res_result['data']['data']['VIPINFOID'],msg="vipinfoid")
                self.assertEqual(data_result[j][2],res_result['data']['data']['VIPNAME'],msg="VIPNAME")
                #self.assertEqual(data_result[j][3],res_result['data']['data']['SEX'],msg="SEX")
                self.assertEqual(data_result[j][4],res_result['data']['data']['MOBILETEL'],msg="MOBILETEL")
                #self.assertEqual(data_result[j][5],res_result['data']['data']['REMARK'],msg="REMARK")
                self.assertEqual(data_result[j][6],res_result['data']['data']['PUTOUTMODE'],msg="PUTOUTMODE")
                self.assertEqual(data_result[j][7],res_result['data']['data']['SHOPCODE'],msg="SHOPCODE")
                self.assertEqual(data_result[j][8],res_result['data']['data']['OPERATOR'],msg="OPERATOR")
                #self.assertEqual(data_result[j][9],res_result['data']['data']['CARDLEVEL'],msg="会员级别")
                self.assertEqual(data_result[j][10],res_result['data']['data']['STATUS'],msg="会员状态")
                #self.assertEqual(data_result[j][11],res_result['data']['data']['FLYMAIL'],msg="微信")     
                self.assertEqual(data_result[j][12],res_result['data']['data']['INTEGRAL'],msg="积分当前")
                self.assertEqual(data_result[j][13],res_result['data']['data']['TOTALINTEGRAL'],msg="累计积分") 
                self.assertEqual(data_result[j][14],res_result['data']['data']['VIPCARDTYPE'],msg="vip类型")
                self.assertEqual(data_result[j][15],res_result['data']['data']['VIPID'],msg="vipid")        

        elif  code == '300':                    
            data_result = db.query(sql.format(mobiletel=mobiletel,vipinfoid=vipinfoid))
            logging.info(data_result)
            self.assertGreaterEqual(len(data_result),2,msg="行数大于等于2")

        elif  code == '400': 
            data_result = db.query(sql.format(mobiletel=mobiletel,vipinfoid=vipinfoid))
            logging.info(data_result)
            for j in range(len(data_result)):
                self.assertIsNotNone(data_result[j][0],msg="cardid不为空")
                self.assertIsNotNone(data_result[j][1],msg="vipinfoid不为空")            
                self.assertEqual(data_result[j][2],data['vipname'],msg="会员名称")
                self.assertEqual(data_result[j][3],data['sex'],msg="性别")
                self.assertEqual(data_result[j][4],data['mobiletel'],msg="会员电话")
                self.assertEqual(data_result[j][6],data['putoutmode'],msg="开卡方式")            
                self.assertEqual(data_result[j][7],data['shopcode'],msg="门店")            
                self.assertEqual(data_result[j][8],data['operator'],msg="开卡人")            
                self.assertIsNotNone(data_result[j][9],msg="会员级别")        
                self.assertEqual(data_result[j][10],1,msg="会员状态") 
                self.assertEqual(data_result[j][11],0,msg="当前积分")            
                self.assertEqual(data_result[j][12],0,msg="累计积分")            
                self.assertIsNotNone(data_result[j][13],msg="开卡状态")            
                self.assertIsNotNone(data_result[j][14],msg="会员ID")            






        return  logging.info('》》》》》》》》》》》》》》》》》》》》》》》》》》》》》断言完成》》》》》》》》》》》》》》》》》》》》》》》》》》》》》')
        
    def checkifexistsvipinfo(self,casename):
        case_data = self.excel.get_test_case(self.data_list,casename)
        case_name = case_data.get('case_name')  
        url = case_data.get('url')
        data = eval(case_data.get('data'))
        if (case_name=='case05'):
            str = '0123456789'
            phone = "159" +"".join(random.choice(str) for i in range(8))
            
            data['mobiletel'] = phone
            
        
        #发送请求
        res = requests.get(url=url,params=data)
        #返回结果，并将json转字符串
        res_dict = json.dumps(res.json(),indent=2,ensure_ascii=False,sort_keys=True)
        #写入日志
        log_case_info(case_name , url , data , res_dict)
        #断言返回码
        #self.assertEqual(res.json()['code'],'200',msg=logging.error('返回码不等于200，OK'))
        #断言
        res_result = res.json()
        code = res.json()['code']
        self.dbassert(code,res_result,data)

    def test_01_checkifexistsvipinfo(self):   
        self.checkifexistsvipinfo("case01")

    def test_02_checkifexistsvipinfo(self):
        self.checkifexistsvipinfo("case02")
    
    def test_03_checkifexistsvipinfo(self):
        self.checkifexistsvipinfo("case03")

    def test_04_checkifexistsvipinfo(self):
        self.checkifexistsvipinfo("case04")

    def test_05_checkifexistsvipinfo(self):
        self.checkifexistsvipinfo("case05")




if __name__=='__main__':   # 如果是直接从当前模块执行（非别的模块调用本模块）
    unittest.main(verbosity=2)    # 运行本测试类所有用例,verbosity为结果显示级别
    