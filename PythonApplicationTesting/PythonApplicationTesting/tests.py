import unittest
from web_manager import web_manager

class TestWebManager(unittest.TestCase):

    def setUp(self):
        self.manager = web_manager()
        f = open("Login_info.txt", 'r')
        username, password = f.readline().split()
        f.close()
        self.manager.Login(username, password)

    def test_Login(self):
        self.assertEqual(self.manager.userId, '1394')

if __name__ == '__main__':
    unittest.main()
