import unittest
from bin.parser import *


class TestLog(unittest.TestCase):

    def test_max_rpm_for_each_transaction(self):
        transactions = ['GET /index.php/backend411/sales_order_invoice/new/order_id/XXXXXX',
                        'POST /index.php/backend411/sales_order_invoice/new/order_id/XXXXXX',
                        'PUT /index.php/backend411/sales_order_invoice/new/order_id/XXXXXX']
        data = read_log('./tests/test_log.log')
        dataframe = replace_dynamic_data(data)
        max_rpm_for_each_transaction = get_max_rpm_for_each_transaction(group_by_transactions(dataframe))
        self.assertEqual(max_rpm_for_each_transaction[transactions[0]], 6)
        self.assertEqual(max_rpm_for_each_transaction[transactions[1]], 4)
        self.assertEqual(max_rpm_for_each_transaction[transactions[2]], 5)

    def test_total_hits_each(self):
        transactions = ['GET /index.php/backend411/sales_order_invoice/new/order_id/XXXXXX',
                        'POST /index.php/backend411/sales_order_invoice/new/order_id/XXXXXX',
                        'PUT /index.php/backend411/sales_order_invoice/new/order_id/XXXXXX']
        data = read_log('./tests/test_log.log')
        dataframe = replace_dynamic_data(data)
        total_hits_each = get_total_hits_for_each_transaction(group_by_transactions(dataframe))
        self.assertEqual(total_hits_each[transactions[0]], 7)
        self.assertEqual(total_hits_each[transactions[1]], 4)
        self.assertEqual(total_hits_each[transactions[2]], 5)

    def test_total_hits(self):
        data = read_log('./tests/test_log.log')
        dataframe = replace_dynamic_data(data)
        total_hits = get_total_hits(dataframe)
        self.assertEqual(total_hits, 16)


if __name__ == '__main__':
    unittest.main()
