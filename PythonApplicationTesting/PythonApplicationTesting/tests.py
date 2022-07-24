import unittest
from web_manager import WebManager

class TestWebManager(unittest.TestCase):

    def setUp(self):
        self.manager = WebManager()
        f = open("Login_info.txt", 'r')
        username, password = f.readline().split()
        f.close()
        self.manager.Login(username, password)

    def test_Login(self):
        self.assertEqual(self.manager.userId, '1394')

if __name__ == '__main__':
    unittest.main()
