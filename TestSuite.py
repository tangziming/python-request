import unittest
from test_checkifexistsvipinfo import Testcheckifexistsvipinfo
from test_GetBillDetails import TestGetBillDetails
from test_GetBillList import TestGetBillList
from test_gethotsalegoodlist import TestGetHotSaleGoodList
from test_getsalestores import Testgetsalestores
from test_payamountdatacommit import Testpayamountdatacommit
from test_ReceiptDataCommit import TestReceiptDataCommit



suite1 = unittest.TestLoader().loadTestsFromTestCase(Testcheckifexistsvipinfo)
suite2 = unittest.TestLoader().loadTestsFromTestCase(TestGetBillDetails)
suite3 = unittest.TestLoader().loadTestsFromTestCase(TestGetBillList)
suite4 = unittest.TestLoader().loadTestsFromTestCase(TestGetHotSaleGoodList)
suite5 = unittest.TestLoader().loadTestsFromTestCase(Testgetsalestores)
suite6 = unittest.TestLoader().loadTestsFromTestCase(Testpayamountdatacommit)
suite7 = unittest.TestLoader().loadTestsFromTestCase(TestReceiptDataCommit)

suite = unittest.TestSuite([suite7,suite6])


#suite = unittest.TestSuite([suite1,suite2,suite3,suite4,suite5])

unittest.TextTestRunner(verbosity=2).run(suite)


