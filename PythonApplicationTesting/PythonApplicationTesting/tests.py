import unittest
from web_manager import WebManager

class TestWebManager(unittest.TestCase):

    def setUp(self):
        self.manager = WebManager()
        f = open("Login_info.txt", 'r')
        username, password = f.readline().split()
        self.manager.spaces_ids = f.readline().split()
        f.close()
        self.manager.login(username, password)

    def test_Login(self):
        self.assertEqual(self.manager.user_id, '1394')

    def test_changing_visibility(self):
        previous = self.manager.is_space_visible(self.manager.spaces_ids[0])
        if previous == True:
            self.manager.edit_space_visibility(self.manager.spaces_ids[0], True, False)
            current = self.manager.is_space_visible(self.manager.spaces_ids[0])
            self.assertNotEqual(previous, current)

            self.manager.edit_space_visibility(self.manager.spaces_ids[0], True, True)
            current = self.manager.is_space_visible(self.manager.spaces_ids[0])
            self.assertEqual(previous, current)
        else:
            self.manager.edit_space_visibility(self.manager.spaces_ids[0], True, True)
            current = self.manager.is_space_visible(self.manager.spaces_ids[0])
            self.assertNotEqual(previous, current)

            self.manager.edit_space_visibility(self.manager.spaces_ids[0], True, False)
            current = self.manager.is_space_visible(self.manager.spaces_ids[0])
            self.assertEqual(previous, current)

if __name__ == '__main__':
    unittest.main()
