import unittest
from test_saveDataV3 import TestSaveDataV3

suite1 = unittest.TestLoader().loadTestsFromTestCase(TestSaveDataV3)


suite = unittest.TestSuite([suite1])

unittest.TextTestRunner(verbosity=2).run(suite)

