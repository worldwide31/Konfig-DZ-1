import os
import tarfile
import sys
import time
import datetime


class ShellEmulator:
    def __init__(self, hostname, vfs_path, start_script_path):
        self.hostname = hostname
        self.vfs_path = vfs_path
        self.start_script_path = start_script_path
        self.current_dir = '/'
        self.vfs = None
        self.load_vfs()

    def load_vfs(self):
        """Загрузка виртуальной файловой системы из TAR архива"""
        if not os.path.exists(self.vfs_path):
            print(f"Error: Virtual file system archive {self.vfs_path} not found.")
            sys.exit(1)

        with tarfile.open(self.vfs_path, 'r') as tar:
            self.vfs = tar.extractall(path='/tmp/virtual_fs')
        print(f"Virtual File System loaded from {self.vfs_path}")

    def run_start_script(self):
        """Выполнение команд из стартового скрипта"""
        if self.start_script_path and os.path.exists(self.start_script_path):
            with open(self.start_script_path, 'r') as script:
                for line in script:
                    line = line.strip()
                    if line:
                        self.execute_command(line)
        else:
            print("Start script not found.")

    def execute_command(self, command):
        """Выполнение команд оболочки"""
        args = command.split()
        cmd = args[0]

        if cmd == "ls":
            self.ls(args)
        elif cmd == "cd":
            self.cd(args)
        elif cmd == "exit":
            self.exit_shell()
        elif cmd == "whoami":
            self.whoami()
        elif cmd == "cal":
            self.cal()
        else:
            print(f"Unknown command: {cmd}")

    def ls(self, args):
        """Команда ls: выводит содержимое текущей директории"""
        path = args[1] if len(args) > 1 else self.current_dir
        if not os.path.exists(path):
            print(f"ls: {path}: No such file or directory")
        else:
            for item in os.listdir(path):
                print(item)

    def cd(self, args):
        """Команда cd: смена текущей директории"""
        if len(args) < 2:
            print("cd: missing argument")
            return

        path = args[1]
        if not os.path.exists(path):
            print(f"cd: {path}: No such file or directory")
        else:
            self.current_dir = path

    def exit_shell(self):
        """Команда exit: выход из эмулятора"""
        print("Exiting shell emulator.")
        sys.exit(0)

    def whoami(self):
        """Команда whoami: выводит имя пользователя"""
        print(f"Current user: {os.getlogin()}")

    def cal(self):
        """Команда cal: выводит текущий календарь"""
        now = datetime.datetime.now()
        print(now.strftime("%B %Y"))
        print(now.strftime("%a  %d %b %Y"))

    def prompt(self):
        """Отображение приглашения для ввода команд"""
        return f"{self.hostname}:{self.current_dir}$ "


def main():
    # Получаем параметры командной строки
    if len(sys.argv) < 4:
        print("Usage: python shell.py <hostname> <vfs_path> <start_script_path>")
        sys.exit(1)

    hostname = sys.argv[1]
    vfs_path = sys.argv[2]
    start_script_path = sys.argv[3]

    emulator = ShellEmulator(hostname, vfs_path, start_script_path)
    emulator.run_start_script()

    # Цикл приема команд
    while True:
        command = input(emulator.prompt())
        emulator.execute_command(command)


if __name__ == "__main__":
    main()
