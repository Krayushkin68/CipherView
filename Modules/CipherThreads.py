import os
from shutil import rmtree
from time import sleep

from PySide2 import QtCore
from PySide2.QtCore import Signal, QThread

from MyCipher import MyCipher


class MySignals(QtCore.QObject):
    update_progress = Signal(int)
    finish = Signal(str)
    pr_size = Signal(int)


def g_list_allfiles(path):
    all_files = []
    dir_list = [path + '\\' + i for i in os.listdir(path)]
    for f in dir_list:
        if os.path.isdir(f):
            all_files.extend(g_list_allfiles(f))
        else:
            all_files.append(f)
    return all_files


class EncrThread(QThread):
    def __init__(self, parent, passw, path):
        QThread.__init__(self, parent)
        self.signals = MySignals()
        self.signals.update_progress.connect(parent.update_pb)
        self.signals.finish.connect(parent.finish)
        self.passw = passw
        self.path = path

    def run(self):
        # Hash
        self.signals.finish.emit('start encryption')
        cipher = MyCipher(self.passw)
        files = g_list_allfiles(self.path)
        self.signals.pr_size.emit(len(files))
        files_h = [cipher.hash_file(f) for f in files]
        with open(self.path + '\\_encdir_\\#hashes.txt', 'w') as h:
            for i in zip(files, files_h):
                if not i[0].endswith('#hashes.txt'):
                    h.write(i[0] + '----' + i[1] + '\n')
        files = g_list_allfiles(self.path)
        self.signals.finish.emit('finished hash')
        # Encrypt
        with open(self.path + '\\_encdir_\\#names.txt', 'w') as n:
            for i, real_name in enumerate(files):
                if os.path.basename(real_name) == '#names.txt':
                    continue
                encr_name = cipher.encrypt_str(real_name)
                hidden_name = os.path.join(self.path, f'File_{i}')  # без папок
                n.write(hidden_name + '-----' + encr_name.decode() + '\n')
                self.signals.update_progress.emit(1)
                cipher.encrypt_file_aes(real_name, hidden_name)
            n.write(self.path + '\\File' + '-----' + 'sysfile' + '\n')
        cipher.encrypt_file_aes(self.path + '\\_encdir_\\#names.txt', self.path + '\\File')  # новое
        # Remove folders
        sleep(0.5)
        path_list = [os.path.join(self.path, i) for i in os.listdir(self.path)]
        for i in path_list:
            if os.path.isdir(i):
                rmtree(i, ignore_errors=True)
        self.signals.finish.emit('finished encryption')


class DecrThread(QThread):
    def __init__(self, parent, passw, path):
        QThread.__init__(self, parent)
        self.signals = MySignals()
        self.signals.update_progress.connect(parent.update_pb)
        self.signals.finish.connect(parent.finish)
        self.passw = passw
        self.path = path

    def run(self):
        # Decrypt
        cipher = MyCipher(self.passw)
        files = g_list_allfiles(self.path)
        self.signals.pr_size.emit(len(files))
        with open(self.path + '\\_encdir_\\#names.txt', 'r') as n:
            while True:
                text = n.readline()
                if len(text) < 10:
                    break
                hidden_name, encr_name = text.strip().split(sep='-----')
                if encr_name == 'sysfile':
                    continue
                real_name = cipher.decrypt_str(encr_name.encode())
                self.signals.update_progress.emit(1)
                # Create folders if not exisitng
                if not os.path.exists(os.path.dirname(real_name)):
                    os.makedirs(os.path.dirname(real_name))
                cipher.decrypt_file_aes(hidden_name, real_name)
        self.signals.finish.emit('finished decryption')
        # Hash
        files = g_list_allfiles(self.path)
        files_h = [cipher.hash_file(f) for f in files]
        with open(self.path + '\\_encdir_\\#hashes.txt', 'w') as h:
            for i in zip(files, files_h):
                if not i[0].endswith('#hashes.txt'):
                    h.write(i[0] + '----' + i[1] + '\n')
        self.signals.finish.emit('finished decrhash')
