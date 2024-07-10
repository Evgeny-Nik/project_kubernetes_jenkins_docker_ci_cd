import unittest
import requests


class TestCase(unittest.TestCase):
    def test_website_connectivity(self):
        try:
            response = requests.get("http://localhost:80")
            self.assertEqual(response.status_code, 200, "Unexpected status code: " + str(response.status_code))
            print("\nRequest successful")

        except requests.exceptions.HTTPError as e:
            self.fail(f'{e.args[0].reason}')
        except requests.exceptions.RequestException as e:
            self.fail(f'{e.args[0].reason}')


if __name__ == '__main__':
    unittest.main()
