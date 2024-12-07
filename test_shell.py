import unittest
from io import StringIO
import sys
import os

from shell import ShellEmulator


class TestShellEmulator(unittest.TestCase):

    def setUp(self):
        # Подготовка временной директории для тестов
        self.temp_dir = '/tmp/test_shell'
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)

    def tearDown(self):
        # Очистка после тестов
        if os.path.exists(self.temp_dir):
            for root, dirs, files in os.walk(self.temp_dir, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(self.temp_dir)

    def test_ls(self):
        """Тестирование команды ls"""
        emulator = ShellEmulator('testhost', '/tmp', None)
        emulator.ls(['ls'])
        # Проверяем вывод команды

    def test_cd(self):
        """Тестирование команды cd"""
        emulator = ShellEmulator('testhost', '/tmp', None)
        emulator.cd(['cd', '/tmp'])
        self.assertEqual(emulator.current_dir, '/tmp')

    def test_whoami(self):
        """Тестирование команды whoami"""
        emulator = ShellEmulator('testhost', '/tmp', None)
        emulator.whoami()

    def test_cal(self):
        """Тестирование команды cal"""
        emulator = ShellEmulator('testhost', '/tmp', None)
        emulator.cal()

    def test_exit(self):
        """Тестирование команды exit"""
        emulator = ShellEmulator('testhost', '/tmp', None)
        with self.assertRaises(SystemExit):
            emulator.exit_shell()

if __name__ == "__main__":
    unittest.main()
