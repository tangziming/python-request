import unittest
from test_ReceiptDataCommit import TestReceiptDataCommit
from test_savePayamount import TestsavePayamount
suite1 = unittest.TestLoader().loadTestsFromTestCase(TestReceiptDataCommit)
suite2 = unittest.TestLoader().loadTestsFromTestCase(TestsavePayamount)

suite = unittest.TestSuite([suite1,suite2])

unittest.TextTestRunner(verbosity=2).run(suite)


