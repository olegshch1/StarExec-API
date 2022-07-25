import unittest
import os
from web_manager import WebManager

class TestWebManager(unittest.TestCase):

    def setUp(self):
        self.manager = WebManager()
        f = open("Login_info.txt", 'r')
        username, password = f.readline().split()
        self.manager.spaces_ids = f.readline().split()
        self.manager.folder_for_downloads = f.readline()
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

    def test_downloading_space(self):
        self.manager.download_space(self.manager.spaces_ids[0], True, True, True)
        dir = os.listdir(self.manager.folder_for_downloads)
        self.assertTrue(len(dir)>0)

if __name__ == '__main__':
    unittest.main()
