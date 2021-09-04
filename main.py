from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtCore import Signal, QThread, Slot, SIGNAL
from MyCipher import MyCipher
from shutil import copyfile, copytree, rmtree
from time import sleep
import os
import gui
import entry
import dialog
import progress


def g_list_allfiles(path):
    all_files = []
    dir_list = [path+'\\'+i for i in os.listdir(path)]
    for f in dir_list:
        if os.path.isdir(f):
            all_files.extend(g_list_allfiles(f))
        else:
            all_files.append(f)
    return all_files


class ShifrView(gui.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self, path, password, new_or_exist):
        super(ShifrView, self).__init__()
        self.path = path
        self.password = password
        self.setupUi(self)
        self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.context_menu)
        self.treeView.doubleClicked.connect(self.TreeDoubleClickEvent)
        self.btn_update.clicked.connect(self.populate(self.path))
        self.btn_check.clicked.connect(self.check_hash)
        self.btn_changekey.clicked.connect(self.change_key)
        self.populate(self.path)
        self.setAcceptDrops(True)
        if new_or_exist == 'new':
            self.create_encdir()
        elif new_or_exist == 'exist':
            self.test_decrypt()

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()

    def dropEvent(self, e):
        for url in e.mimeData().urls():
            file_name = url.toLocalFile()
            p = e.pos()
            p.setY(p.y() - 35)
            self.treeView.setCurrentIndex(self.treeView.indexAt(p))
            cur_path = self.model.filePath(self.treeView.currentIndex())
            if not cur_path:
                cur_path = self.path
            elif not os.path.isdir(cur_path):
                cur_path = os.path.dirname(cur_path)
            if os.path.isdir(file_name):
                copytree(file_name, cur_path+'\\'+os.path.basename(file_name))
            else:
                copyfile(file_name, cur_path + '\\' + os.path.basename(file_name))

    def create_encdir(self):
        try:
            os.mkdir(self.path+'\\_encdir_')
        except Exception:
            if os.path.exists(self.path+'\\_encdir_\\#names.txt.crypt'):
                msgBox = QtWidgets.QMessageBox()
                msgBox.setText('Папка уже является зашифрованной, пытаюсь расшифровать...')
                msgBox.exec_()
                self.test_decrypt()
                return
        global fd
        fd = True
        self.show()

    def test_decrypt(self):
        cipher = MyCipher(self.password)
        test_file = self.path + '\\File'
        copy_test = self.path + '\\File_copy'
        if os.path.exists(test_file):
            with open(test_file, 'rb') as test, open(copy_test, 'wb') as copy:
                copy.write(test.read())
                try:
                    os.mkdir(self.path + '\\_encdir_')
                except FileExistsError:
                    pass
            if cipher.decrypt_file_aes(copy_test, self.path + '\\_encdir_\\#names.txt') != 'error':
                os.remove(test_file)
                global pb
                pb = Progress(self.password, self.path)
                pb.show()
                pb.setFocus()
                pb.start_dec_thr()
            else:
                msgBox = QtWidgets.QMessageBox()
                msgBox.setText('Ошибка расшифрования, неверный ключ!')
                os.remove(self.path + '\\_encdir_\\#names.txt')
                os.remove(copy_test)
                rmtree(self.path + '\\_encdir_')
                msgBox.exec_()  # сделать возврат на главный экран
                app.exit()
        else:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText('Отсутствует тестовый файл!\nПожалйста, создайте шифрованную папку заново.')
            msgBox.exec_()
            print('нет names')
            app.exit()

    def TreeDoubleClickEvent(self, index):
        cur_path = self.model.filePath(index)
        if not os.path.isdir(cur_path):
            os.startfile(cur_path)

    def populate(self, path):
        self.model = QtWidgets.QFileSystemModel()
        self.model.setRootPath((QtCore.QDir.rootPath()))
        self.treeView.setModel(self.model)
        self.treeView.setRootIndex(self.model.index(path))
        self.treeView.setSortingEnabled(True)
        self.treeView.sortByColumn(0, QtCore.Qt.AscendingOrder)
        self.treeView.setColumnWidth(0, 220)
        self.treeView.setColumnWidth(1, 50)
        self.treeView.setColumnWidth(2, 50)
        self.treeView.setColumnWidth(3, 110)

    def context_menu(self):
        menu = QtWidgets.QMenu()
        op = menu.addAction('Открыть')
        op.triggered.connect(self.open_file)
        de = menu.addAction('Удалить')
        de.triggered.connect(self.del_file)
        cursor = QtGui.QCursor()
        menu.exec_(cursor.pos())

    def open_file(self):
        index = self.treeView.currentIndex()
        file_path = self.model.filePath(index)
        os.startfile(file_path)

    def del_file(self):
        index = self.treeView.currentIndex()
        file_path = self.model.filePath(index)
        os.remove(file_path)

    def change_key(self):
        cur_pass, ok1 = QtWidgets.QInputDialog.getText(self, "Смена ключа",
                                                  "Введите действующий ключ:", QtWidgets.QLineEdit.Password)
        if ok1 and cur_pass == self.password:
            new_pass, ok2 = QtWidgets.QInputDialog.getText(self, "Смена ключа",
                                                           "Введите новый ключ:", QtWidgets.QLineEdit.Password)
            if ok2:
                if not new_pass:
                    QtWidgets.QMessageBox.warning(self, "Смена ключа", "Ключ не может быть пустым!!!")
                    return
                self.password = new_pass
                self.cipher = MyCipher(new_pass)
                QtWidgets.QMessageBox.information(self, "Смена ключа", "Ключ успешно изменен")
        elif ok1 and cur_pass != self.password:
            QtWidgets.QMessageBox.warning(self, "Смена ключа", "Неверный текущий ключ!!!")

    def check_hash(self):
        if not os.path.exists(self.path + '\\_encdir_\\#hashes.txt'):
            QtWidgets.QMessageBox.information(self, "Проверка хэша", 'Данная функция будет доступна '
                                                                     'после перезапуска программы...')
            return
        sw.statusBar.showMessage('Проверяем хэши файлов...',2000)
        cipher = MyCipher(self.password)
        files = g_list_allfiles(self.path)
        files_h = [cipher.hash_file(f) for f in files]
        f_dict = dict(zip(files, files_h))
        corrupted = []
        with open(self.path + '\\_encdir_\\#hashes.txt', 'r') as h:
            current = []
            while True:
                text = h.readline()
                if len(text) < 10:
                    break
                current.append(tuple(text.strip().split(sep='----')))
        for i in current:
            if f_dict.get(i[0]) != i[1] and not i[0].endswith('#hashes.txt'):
                corrupted.append(i)
        msgBox = QtWidgets.QMessageBox()
        sw.statusBar.showMessage('Проверка завершена', 2000)
        if not corrupted:
            msgBox.setText('Файлы в Ваше отсутствие не изменялись.\nХэши совпадают.')
        else:
            cor_str = ''
            for i in corrupted:
                cor_str += f'{i[0]}\n'
            msgBox.setText('Обнаружены изменения в файлах:\n'+cor_str)
        msgBox.exec_()

    def closeEvent(self, event:QtGui.QCloseEvent):
        event.ignore()
        if not fd:
            QtWidgets.QMessageBox.warning(self, "Закрытие", 'Еще не закончилось стартовое хэширование, подождите...')
            return
        # Проверка на открытые файлы
        files = g_list_allfiles(self.path)
        opened=[]
        for f in files:
            try:
                fo = open(f,'a+')
                fo.close()
            except IOError:
                opened.append(f)
        if opened:
            s = 'Закройте следующие файлы перед завершением работы программы:\n'
            for o in opened:
                s += o+'\n'
            QtWidgets.QMessageBox.warning(self, "Закрытие", s)
            event.ignore()
        else:
            # Запуск шифрования
            global pb
            pb = Progress(self.password, self.path)
            pb.start_enc_thr()


class MySignals(QtCore.QObject):
    update_progress = Signal(int)
    finish = Signal(str)
    pr_size = Signal(int)


class EncrThread(QThread):
    def __init__(self, parent, passw, path):
        QThread.__init__(self, parent)
        self.signals = MySignals()
        self.signals.update_progress.connect(parent.update_pb)
        self.signals.finish.connect(parent.finish)
        self.passw = passw
        self.path = path

    def run(self):
        # Хэширую
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
        # Шифрую
        with open(self.path + '\\_encdir_\\#names.txt', 'w') as n:
            for i, real_name in enumerate(files):
                if os.path.basename(real_name) == '#names.txt':
                    continue
                encr_name = cipher.encrypt_str(real_name)
                hidden_name = os.path.join(self.path, f'File_{i}')    # без папок
                n.write(hidden_name+'-----'+encr_name.decode()+'\n')
                self.signals.update_progress.emit(1)
                cipher.encrypt_file_aes(real_name, hidden_name)
            n.write(self.path + '\\File' + '-----' + 'sysfile' + '\n')
        cipher.encrypt_file_aes(self.path + '\\_encdir_\\#names.txt', self.path + '\\File')      # новое
        # удалить папки
        sleep(0.5)
        path_list = [os.path.join(self.path, i) for i in os.listdir(self.path)]
        print(path_list)
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
        # Дешифрую
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
                # создать папки если их нет
                if not os.path.exists(os.path.dirname(real_name)):
                    os.makedirs(os.path.dirname(real_name))
                cipher.decrypt_file_aes(hidden_name, real_name)
        self.signals.finish.emit('finished decryption')
        # Хэширую
        files = g_list_allfiles(self.path)
        files_h = [cipher.hash_file(f) for f in files]
        with open(self.path + '\\_encdir_\\#hashes.txt', 'w') as h:
            for i in zip(files, files_h):
                if not i[0].endswith('#hashes.txt'):
                    h.write(i[0] + '----' + i[1] + '\n')
        self.signals.finish.emit('finished decrhash')


class EntryWindow(entry.Ui_EntryWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super(EntryWindow, self).__init__()
        self.setupUi(self)
        self.btn_exist.clicked.connect(self.open_exist)
        self.btn_new.clicked.connect(self.open_new)

    def open_exist(self):
        self.hide()
        global dw
        dw = DialogWindow('exist')
        dw.setFixedSize(dw.size())
        dw.setWindowTitle('Открытие существующей')
        dw.show()

    def open_new(self):
        self.hide()
        global dw
        dw = DialogWindow('new')
        dw.setFixedSize(dw.size())
        dw.setWindowTitle('Выбор папки для шифрования')
        dw.show()


class DialogWindow(dialog.Ui_Dialog_open, QtWidgets.QMainWindow):
    def __init__(self, new_or_exist):
        super(DialogWindow, self).__init__()
        self.setupUi(self)
        self.new_or_exist = new_or_exist
        self.btn_ok.clicked.connect(self.ok)
        self.btn_cancel.clicked.connect(self.cancel)
        self.btn_obzor.clicked.connect(self.obzor)
        # self.Edit_path.setText('C:\\Users\\User\\PycharmProjects\\ShifrView\\Test')  ###############################################
        # self.Edit_passwd.setText('password')  ###############################################

    def ok(self):
        self.path = self.Edit_path.text()
        self.password = self.Edit_passwd.text()
        global sw
        sw =ShifrView(self.path, self.password, self.new_or_exist)
        sw.setFixedHeight(465)
        sw.setFixedWidth(452)
        enw.destroy()
        self.destroy()

    def cancel(self):
        enw.show()
        self.close()

    def obzor(self):
        qf = QtWidgets.QFileDialog()
        path = qf.getExistingDirectory().replace('/', '\\')
        self.Edit_path.setText(path)

    def closeEvent(self, event: QtGui.QCloseEvent):
        self.hide()
        enw.show()
        event.accept()


class Progress(progress.Ui_ProgressCipher, QtWidgets.QMainWindow):
    def __init__(self, passw, path):
        super(Progress, self).__init__()
        self.setupUi(self)
        self.passw = passw
        self.path = path

    @Slot(int)
    def update_pb(self, val):
        self.progressBar.setValue(self.progressBar.value() + val)

    @Slot(int)
    def pr_size(self, val):
        self.progressBar.setMaximum(val)

    @Slot(str)
    def finish(self, fin):
        global fd
        self.progressBar.setValue(self.progressBar.maximum())
        if fin == 'finished encryption':
            app.exit()
        elif fin == 'finished decryption':
            sw.statusBar.showMessage('Хэшируем файлы...')
            sw.show()
            self.destroy()
        elif fin == 'start decryption':
            fd = False
        elif fin == 'finished hash':
            sw.statusBar.clearMessage()
            sw.statusBar.showMessage('Хэширование завершено.', 2000)
            self.progressBar.setValue(0)
            self.show()
            self.setFocus()
            self.label.setText('Производится шифрование...')
        elif fin == 'finished decrhash':
            fd = True
            sw.statusBar.clearMessage()
            sw.statusBar.showMessage('Хэширование завершено.', 2000)

    def start_enc_thr(self):
        sw.statusBar.showMessage('Хэшируем файлы...')
        self.label.setText('Производится хэширование...')
        self.setWindowTitle('Шифрование')
        thr = EncrThread(self, self.passw, self.path)
        thr.start()

    def start_dec_thr(self):
        self.label.setText('Производится расшифрование...')
        self.setWindowTitle('Расшифрование')
        thr = DecrThread(self, self.passw, self.path)
        thr.start()


if __name__ == '__main__':
    fd = False
    app = QtWidgets.QApplication([])
    enw = EntryWindow()
    enw.setFixedSize(enw.size())
    enw.show()
    app.exec_()
