import unittest
from bin.parser import *


class TestLog(unittest.TestCase):
    def test_max_rpm_for_each_transaction(self):
        transactions = ['GET /index.php/backend411/sales_order_invoice/new/order_id/XXXXXX',
                        'POST /index.php/backend411/sales_order_invoice/new/order_id/XXXXXX',
                        'PUT /index.php/backend411/sales_order_invoice/new/order_id/XXXXXX']
        p = Parser('./data/test_log.log')
        max_rpm_for_each_transaction = p.get_max_rpm_for_each_transaction(p.group_by_transactions())
        self.assertEqual(max_rpm_for_each_transaction[transactions[0]], 6)
        self.assertEqual(max_rpm_for_each_transaction[transactions[1]], 3)
        self.assertEqual(max_rpm_for_each_transaction[transactions[2]], 5)

    def test_total_hits_each(self):
        transactions = ['GET /index.php/backend411/sales_order_invoice/new/order_id/XXXXXX',
                        'POST /index.php/backend411/sales_order_invoice/new/order_id/XXXXXX',
                        'PUT /index.php/backend411/sales_order_invoice/new/order_id/XXXXXX']
        p = Parser('./data/test_log.log')
        total_hits_each = p.get_total_hits_for_each_transaction(p.group_by_transactions())
        self.assertEqual(total_hits_each[transactions[0]], 7)
        self.assertEqual(total_hits_each[transactions[1]], 4)
        self.assertEqual(total_hits_each[transactions[2]], 5)

    def test_total_hits(self):
        p = Parser('./data/test_log.log')
        self.assertEqual(p.get_total_hits(p.dataframe), 16)

    def test_max_rpm_for_all_transactions(self):
        p = Parser('./data/test_log.log')
        self.assertEqual(p.get_max_rpm_for_all_transactions(), 7)


if __name__ == '__main__':
    unittest.main()
