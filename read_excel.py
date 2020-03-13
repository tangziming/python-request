import xlwt 
import xlrd 
from xlutils.copy import copy




class Excel():

    def __init__(self,file_name):
        #打开excel文件
        self.file_name = file_name
        self.wb = xlrd.open_workbook(file_name,formatting_info=True)

    
    def get_sheet_list(self,sheet):
        '''获取工作表的数据 返回值是列表'''
        #   定义一个空列表
        data_list=[]
        #   按工作簿名定位工作表
        sh = self.wb.sheet_by_name(sheet)
        #   获取表头
        header = sh.row_values(0)
        
        for i in range(1,sh.nrows):
            #将表头和每一行的数据，打包成元祖的列表，然后转成字典
            d = dict(zip(header,sh.row_values(i)))
            #讲字典追加到列表
            data_list.append(d)
        return data_list



    def get_test_case(self,data_list,case_name):
        '''从数据列表里 根据用例名称获取相应数据'''
        msg = "找不到该用例"
        for case_data in data_list:
            if case_name == case_data['case_name']:
                print(case_data['case_name'])
                return case_data

        print(case_data['case_name'])
        return msg

    def get_header_col(self,sheet_name,header):
        '''获取表头在第几列  （参数：1、工作表名称；2、表头名称）''' 
        sheet = self.wb.sheet_by_name(sheet_name)
        #获取最大的列
        max_col = sheet.ncols
        for col in range(max_col):
            if sheet.cell(0,col).value == header:
                return col

    def get_sheet_index_by_name(self,sheet_name):
        """Get a sheet by name from xlwt.Workbook, a strangely missing method.
        Returns None if no sheet with the given name is present.
        """
        # Note, we have to use exceptions for flow control because the
        # xlwt API is broken and gives us no other choice.

        #获取sheet长度
        sheet_len = len(self.wb.sheets())
        try:
            for index in range(sheet_len):
                sheet = self.wb.sheet_by_index(index)
                if sheet.name == sheet_name:
                    return index
        except IndexError:
            return None


    def excel_write(self,sheet_name,header,content): 

        sheet = self.wb.sheet_by_name(sheet_name)
        max_row = sheet.nrows

        new_wb = copy(self.wb)
        sheet_index = Excel.get_sheet_index_by_name(self,sheet_name)
        new_sheet = new_wb.get_sheet(sheet_index)

        header_col = Excel.get_header_col(self,sheet_name,header)
        print(header_col)
        for i in range(1,max_row):
            new_sheet.write(i,header_col,content[i-1])
      
        new_wb.save(self.file_name)
        print("数据写入成功")
        
        return None

    def excel_replace(self,sheet_name,new_target,replace,old_target):

        sheet = self.wb.sheet_by_name(sheet_name)
        max_row = sheet.nrows

        new_wb = copy(self.wb)
        sheet_index = Excel.get_sheet_index_by_name(self,sheet_name)
        new_sheet = new_wb.get_sheet(sheet_index)

        for i in range(1,max_row):
            replace_col = Excel.get_header_col(self,sheet_name,replace)
            new_target_col = Excel.get_header_col(self,sheet_name,new_target)
            old_target_col = Excel.get_header_col(self,sheet_name,old_target)

            replace_value = sheet.cell(i,replace_col).value
            new_target_value = sheet.cell(i,new_target_col).value
            old_target_value = sheet.cell(i,old_target_col).value

            new_target_value = new_target_value.replace(old_target_value,replace_value)
            new_sheet.write(i,new_target_col,new_target_value)
            new_sheet.write(i,old_target_col,replace_value )
        new_wb.save(self.file_name)
        print("数据替换成功")

        return None





if __name__ == '__main__':
    #实例化Excel类
    excel = Excel("testcase.xls")
    #打印表头'oldbillid' 在哪一列
    #print(excel.get_header_col("PayamountDataCommit","oldbillid"))
    #打印TestSaveDataV3工作表的数据
    #sheet_list = excel.get_sheet_list("TestSaveDataV3")
    #print(sheet_list)
    #从TestSaveDataV3工作表的数据里 根据用例名称获取相应数据
    #print(excel.get_test_case(sheet_list,"savedate_normal"))

    #获取sheet的index
    #print(excel.get_sheet_by_name("Sheet3"))

    #写入内容到执行列
    #excel.excel_write("PayamountDataCommit","newbillid",["AAAAAA1","BBBBBB1","CCCCCC2"])

    #匹配数据进行替换
    #excel.excel_replace("PayamountDataCommit","data","newbillid","oldbillid")
    




















