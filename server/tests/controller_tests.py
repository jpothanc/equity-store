import unittest

from parameterized import parameterized

from main import eq_app
class ControllerTestCase(unittest.TestCase):
    def setUp(self):
        self.client = eq_app.test_client()
        self.client.testing = True

    @parameterized.expand([
        ("0005.HK", 200),
        ("XXX.TW", 404),
    ])
    def test_get_equity_by_product_code_returns_correct_product_code(self, product_code, expected_status):
        response = self.client.get(f'/api/v1/equity?product_code={product_code}')
        self.assertEqual(response.status_code, expected_status)
        if response.status_code == 200:
            data = response.get_json()
            self.assertEqual(data['product_code'], product_code)

    @parameterized.expand([
        ("HKSE", 200),
        ("XXXX", 404),
    ])
    def test_get_equity_by_exchange_returns_correct_exchange_products(self, exchange_code, expected_status):
        response = self.client.get(f'/api/v1/equity/exchange?exchange_code={exchange_code}')
        self.assertEqual(response.status_code, expected_status)
        if response.status_code == 200:
            data = response.get_json()
            # self.assertGreater(len(data), 0)


if __name__ == '__main__':
    unittest.main()
