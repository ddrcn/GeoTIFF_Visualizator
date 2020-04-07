import os, gc
import sys
import cv2
import shutil
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from UI.mainwindow import *
import SobelCV


class AppWindow(QMainWindow, Ui_MainWindow):
    file = None
    kernel_size = 3
    img = None
    output_img = None

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.change_button(False)
        self.action.triggered.connect(self.load_file)
        self.action_X_Y.triggered.connect(self.save_file_xy)
        self.action_Y.triggered.connect(self.save_file_y)
        self.action_3.triggered.connect(self.save_file_x)
        self.action_4.triggered.connect(self.save_file_schar)
        self.init_buttons()

    def init_buttons(self):
        self.pushButton.clicked.connect(self.apply_filter_xy)
        self.pushButton_3.clicked.connect(self.apply_filter_x)
        self.pushButton_4.clicked.connect(self.apply_filter_y)
        self.pushButton_2.clicked.connect(self.disable_filter)
        self.pushButton_6.clicked.connect(self.add_kernel)
        self.pushButton_5.clicked.connect(self.sub_kernel)
        self.pushButton_7.clicked.connect(self.apply_schar)
        self.label_2.setText('Размер ядра Собеля: ' + str(self.kernel_size))
        self.label.setText('Загрузите файл')

    def change_button(self, var):
        self.pushButton.setEnabled(var)
        self.pushButton_2.setEnabled(var)
        self.pushButton_3.setEnabled(var)
        self.pushButton_4.setEnabled(var)
        self.pushButton_5.setEnabled(True)
        self.pushButton_6.setEnabled(True)
        self.pushButton_7.setEnabled(var)
        self.action_X_Y.setEnabled(False)
        self.action_Y.setEnabled(False)
        self.action_3.setEnabled(False)
        self.action_4.setEnabled(False)

    def load_file(self):
        gc.collect()
        self.label.setText('Без фильтра')
        self.img = None
        self.file = None
        self.action_X_Y.setEnabled(False)
        self.action_Y.setEnabled(False)
        self.action_3.setEnabled(False)
        self.action_4.setEnabled(False)
        try:
            self.file =\
                QFileDialog.getOpenFileName(QFileDialog(), 'Open file', '/home', 'Files(*.tif *.tiff *.jpg *.jpeg)')[0]
        except Exception:
            self.file = None
        if (self.file is not None and self.file != ''):
            if (os.path.exists('.temp')):
                shutil.rmtree('.temp')
            self.change_button(True)
            self.print_file()
            os.mkdir('.temp')
            shutil.copy(self.file, '.temp/default.tif')
            self.output_img = '.temp/default.tif'
            self.img = cv2.imread(self.file, 0)
            SobelCV.path = '.temp/'
            SobelCV.auto_create_all(self.img, '.temp/', self.kernel_size)

    def print_file(self):
        self.label_3.setPixmap(QPixmap(self.file))
        self.label_3.setScaledContents(True)

    def closeEvent(self, *args, **kwargs):
        if (os.path.exists('.temp')):
            shutil.rmtree('.temp')

    def apply_filter_xy(self):
        self.label_3.setPixmap(QPixmap('.temp/xy.tif'))
        self.output_img = '.temp/xy.tif'
        self.action_X_Y.setEnabled(True)
        self.label.setText('Фильтр Собеля по X и Y')

    def apply_filter_x(self):
        self.label_3.setPixmap(QPixmap('.temp/x.tif'))
        self.output_img = '.temp/x.tif'
        self.action_3.setEnabled(True)
        self.label.setText('Фильтр Собеля по X')

    def apply_filter_y(self):
        self.label_3.setPixmap(QPixmap('.temp/y.tif'))
        self.output_img = '.temp/y.tif'
        self.action_Y.setEnabled(True)
        self.label.setText('Фильтр Собеля по Y')

    def disable_filter(self):
        self.label_3.setPixmap(QPixmap('.temp/default.tif'))
        self.output_img = '.temp/default.tif'
        self.label.setText('Без фильтра')

    def add_kernel(self):
        self.pushButton_5.setEnabled(True)
        if (self.kernel_size < 9):
            self.kernel_size += 2
            self.label_2.setText('Размер ядра Собеля: ' + str(self.kernel_size))
            # SobelCV.auto_create_all(self.img, '.temp/', self.kernel_size)
            # self.label_3.setPixmap(QPixmap(self.output_img))
            if (self.kernel_size == 9):
                self.pushButton_6.setEnabled(False)

    def sub_kernel(self):
        self.pushButton_6.setEnabled(True)
        if (self.kernel_size > 1):
            self.kernel_size -= 2
            self.label_2.setText('Размер ядра Собеля: ' + str(self.kernel_size))
            # SobelCV.auto_create_all(self.img, '.temp/', self.kernel_size)
            # self.label_3.setPixmap(QPixmap(self.output_img))
            if (self.kernel_size == 1):
                self.pushButton_5.setEnabled(False)

    def apply_schar(self):
        self.label_3.setPixmap(QPixmap('.temp/xy_schar.tif'))
        self.output_img = '.temp/xy_schar.tif'
        self.action_4.setEnabled(True)
        self.label.setText('Фильтр Шарра по X и Y')

    def save_file_xy(self):
        path = QFileDialog.getSaveFileName(QFileDialog(), 'Save file', '/home', 'Files(*.tif *.tiff *.jpg *.jpeg)')
        try:
            shutil.copy('.temp/xy.tif', path[0])
        except Exception:
            print('Ошибка сохранения')

    def save_file_x(self):
        path = QFileDialog.getSaveFileName(QFileDialog(), 'Save file', '/home', 'Files(*.tif *.tiff *.jpg *.jpeg)')
        try:
            shutil.copy('.temp/x.tif', path[0])
        except Exception:
            print('Ошибка сохранения')

    def save_file_y(self):
        path = QFileDialog.getSaveFileName(QFileDialog(), 'Save file', '/home', 'Files(*.tif *.tiff *.jpg *.jpeg)')
        try:
            shutil.copy('.temp/y.tif', path[0])
        except Exception:
            print('Ошибка сохранения')

    def save_file_schar(self):
        path = QFileDialog.getSaveFileName(QFileDialog(), 'Save file', '/home', 'Files(*.tif *.tiff *.jpg *.jpeg)')
        try:
            shutil.copy('.temp/xy_schar.tif', path[0])
        except Exception:
            print('Ошибка сохранения')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AppWindow()
    window.show()
    sys.exit(app.exec_())
