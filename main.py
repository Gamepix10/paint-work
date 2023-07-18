import sys
import os
import all
import re
from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore, QtWidgets
from PIL import Image, ImageFont
from keras import layers
from keras import models
import matplotlib.pyplot as plt
import sys
import random
from PIL import ImageDraw
from PIL import Image, ImageOps
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from keras.datasets import mnist
from lab5 import Matrita
from pathlib import Path
(train_image, train_labels), (test_image, test_labels) = mnist.load_data()
global imggggg


class Paint(QtWidgets.QMainWindow, all.Ui_MainWindow):

    def __init__(self, parent=None):
        super(Paint, self).__init__(parent)
        uic.loadUi('all.ui', self)

        self.photo_w = 700
        self.photo_h = 650
        global imggggg
        imggggg = 0

        self.background = Qt.white

        title = "minipaint"

        self.setWindowTitle(title)
        self.setFixedSize(870, 658)
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)

        self.drawing = False
        self.color = Qt.black
        self.brushSize = 2
        self.brushColor = Qt.black
        self.LastPoint = QPoint()

        self.setupUi(self)
        self.btn_browse.triggered.connect(self.browse_file)
        self.btn_left.clicked.connect(self.left_photo)
        self.btn_right.clicked.connect(self.right_photo)
        self.photo.resize(QSize(self.photo_w, self.photo_h))

        # if (imggggg == 0):
        # self.image = QImage(self.size(), QImage.Format_RGB32)
        # self.image.fill(Qt.white)
       # else:
        # print(imggggg)
        # self.image = QImage(imggggg)
        # self.image = self.image.scaled(700, 600)

        self.actionSave.triggered.connect(self.save)

        self.actionExit_2.triggered.connect(self.exit)

        self.actionClose.triggered.connect(self.clear)

        self.actionOpen_Pallete.triggered.connect(self.open_pallete)

        self.action3px.triggered.connect(self.three_px)

        self.action3px_2.triggered.connect(self.eraser_3)

        self.action5px.triggered.connect(self.five_px)

        self.action5px_2.triggered.connect(self.eraser_5)

        self.action7px.triggered.connect(self.seven_px)

        self.action7px_2.triggered.connect(self.eraser_7)

        self.action9px.triggered.connect(self.nine_px)

        self.action9px_2.triggered.connect(self.eraser_9)

        self.action11px.triggered.connect(self.eraser_11)

        self.action15px.triggered.connect(self.eraser_15)

        self.actionReliz.triggered.connect(self.define)

        self.actionOttenki_Serogo.triggered.connect(self.Ottenki_Serogo)

        self.actionNegtive.triggered.connect(self.Negative)

        self.actionShum.triggered.connect(self.Shum)

        self.actionSepia.triggered.connect(self.Sepia)

        self.actionBlack_White.triggered.connect(self.Black_White)

        self.actionYarkost.triggered.connect(self.Yarkosty)

        self.actionSlojenie.triggered.connect(self.plus)

        self.actionVichitanie.triggered.connect(self.minus)

        self.actionUmnojenia.triggered.connect(self.umnozenie)

        self.actionDelenie.triggered.connect(self.delenie)

        self.actionCareliatia_Svertka.triggered.connect(self.Matrita)

        self.actionSet_Text.triggered.connect(self.vstavka)

        self.actionWorkwithShum.triggered.connect(self.rabota_s_shumami)

    def browse_file(self):
        global imggggg
        directory = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Выберите папку")
        self.num_photo = 0
        self.arr_photo = []
        extension = ['.png', '.jpeg.', '.jpg', '.bmp', '.gif']
        if directory:
            for file in os.listdir(directory):
                _, file_extension = os.path.splitext(file)
                if file_extension in extension:
                    self.arr_photo.append(directory + '/' + file)

        # print(self.arr_photo)
        if len(self.arr_photo) != 0:
            self.image = QImage(QPixmap(self.arr_photo[0]))
            self.image = self.image.scaled(870, 658)
            imggggg = self.arr_photo[0]
            self.resize_photo()

    def left_photo(self):
        global imggggg
        if len(self.arr_photo) > 1:
            self.num_photo -= 1
            if self.num_photo < 0:
                self.num_photo = len(self.arr_photo) - 1
            self.image = QImage(QPixmap(self.arr_photo[self.num_photo]))
            self.image = self.image.scaled(870, 658)
            imggggg = self.arr_photo[self.num_photo]
            self.resize_photo()
            self.update()

    def right_photo(self):
        global imggggg
        if len(self.arr_photo) > 1:
            self.num_photo += 1
            if self.num_photo == len(self.arr_photo):
                self.num_photo = 0
            self.image = QImage(QPixmap(self.arr_photo[self.num_photo]))
            self.image = self.image.scaled(870, 658)
            imggggg = self.arr_photo[self.num_photo]
            self.resize_photo()
            self.update()

    def resize_photo(self):
        (width_photo, height_photo) = Image.open(
            self.arr_photo[self.num_photo]).size
        #print(width_photo, height_photo)
        if width_photo > height_photo:
            photo_res_w = self.photo_w
            photo_res_h = int((height_photo / width_photo * self.photo_w)//1)
            photo_move_w = 0
            photo_move_h = (self.photo_h - photo_res_h) // 2
        else:
            photo_res_h = self.photo_h
            photo_res_w = int((width_photo / height_photo * self.photo_h)//1)
            photo_move_w = (self.photo_w - photo_res_w) // 2
            photo_move_h = 0
        self.photo.resize(QSize(photo_res_w, photo_res_h))
        self.photo.move(50 + photo_move_w, 10 + photo_move_h)
        self.photo.show()

    def exit(self):
        exit()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.LastPoint = event.pos()

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) & self.drawing:
            painter = QPainter(self.image)
            painter.setPen(QPen(self.brushColor, self.brushSize,
                           Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.LastPoint, event.pos())
            self.LastPoint = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())

    def save(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                                                   "File PNG(*.png);;File JPEG(*.jpg *.jpeg);;All Files(*.*) ")

        if file_path == "":
            return
        self.image.save(file_path)

    def clear(self):
        self.image.fill(self.background)
        self.update()

    def three_px(self):
        self.brushColor = self.color
        self.brushSize = 3

    def five_px(self):
        self.brushColor = self.color
        self.brushSize = 5

    def seven_px(self):
        self.brushColor = self.color
        self.brushSize = 7

    def nine_px(self):
        self.brushColor = self.color
        self.brushSize = 9

    def eraser_3(self):
        self.brushSize = 3
        self.brushColor = self.background

    def eraser_5(self):
        self.brushSize = 5
        self.brushColor = self.background

    def eraser_7(self):
        self.brushSize = 7
        self.brushColor = self.background

    def eraser_9(self):
        self.brushSize = 9
        self.brushColor = self.background

    def eraser_11(self):
        self.brushSize = 11
        self.brushColor = self.background

    def eraser_15(self):
        self.brushSize = 15
        self.brushColor = self.background

    def open_pallete(self):
        self.color = QColorDialog.getColor()
        if self.color.isValid():
            self.brushColor = self.color

    def define(self):
        self.image = self.image.scaled(28, 28)
        self.img = self.image.save("temp.png")
        img = Image.open("temp.png")
        img = img.convert('L')
        img = np.array(img)
        img = 255 - img
        test_image = img.reshape((1, 28*28))
        print(img)

        model = models.load_model("test.h5")

        prediction = model.predict(test_image)
        for i in range(len(prediction)):
            print(prediction[i], " ",)
            # plt.show()
        print(np.argmax(prediction))
        self.image = self.image.scaled(870, 658)

    def Ottenki_Serogo(self):
        image = Image.open(self.arr_photo[self.num_photo])
        draw = ImageDraw.Draw(image)
        width = image.size[0]
        height = image.size[1]
        pix = image.load()
        for i in range(width):
            for j in range(height):
                a = pix[i, j][0]
                b = pix[i, j][1]
                c = pix[i, j][2]
                S = int((a+b+c)/3)
                draw.point((i, j), (S, S, S))
        filePath, _ = QFileDialog.getSaveFileName(
            self, "Save", "", "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
        if filePath == "":
            return
        image.save(filePath)
        image.show()

    def Negative(self):
        image = Image.open(self.arr_photo[self.num_photo])
        draw = ImageDraw.Draw(image)
        width = image.size[0]
        height = image.size[1]
        pix = image.load()
        for i in range(width):
            for j in range(height):
                a = pix[i, j][0]
                b = pix[i, j][1]
                c = pix[i, j][2]
                draw.point((i, j), (255-a, 255-b, 255-c))
        filePath, _ = QFileDialog.getSaveFileName(
            self, "Save", "", "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
        if filePath == "":
            return
        image.save(filePath)
        image.show()

    def Shum(self):
        image = Image.open(self.arr_photo[self.num_photo])
        draw = ImageDraw.Draw(image)
        width = image.size[0]
        height = image.size[1]
        pix = image.load()
        k, okPressed = QInputDialog.getInt(
            self, "Уровень шума", "Введите положительное значение:", 0, 0, 10000, 1)
        if okPressed:
            self.shum = k
        else:
            return
        for i in range(width):
            for j in range(height):
                rand = random.randint(-self.shum, self.shum)
                a = pix[i, j][0]+rand
                b = pix[i, j][1]+rand
                c = pix[i, j][2]+rand
                draw.point((i, j), (a, b, c))
        filePath, _ = QFileDialog.getSaveFileName(
            self, "Save", "", "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
        if filePath == "":
            return
        image.save(filePath)
        image.show()

    def Sepia(self):
        image = Image.open(self.arr_photo[self.num_photo])
        draw = ImageDraw.Draw(image)
        width = image.size[0]
        height = image.size[1]
        pix = image.load()
        t, okPressed = QInputDialog.getInt(
            self, "Уровень сепии", "Введите значение:", 0, -10000, 10000, 1)
        if okPressed:
            self.koef = t
        else:
            return
        for i in range(width):
            for j in range(height):
                a = pix[i, j][0]
                b = pix[i, j][1]
                c = pix[i, j][2]
                S = int((a + b + c) / 3)
                a = S + 2 * self.koef
                b = S + self.koef
                c = S
                draw.point((i, j), (a, b, c))
        filePath, _ = QFileDialog.getSaveFileName(
            self, "Save", "", "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
        if filePath == "":
            return
        image.save(filePath)
        image.show()

    def Black_White(self):
        image = Image.open(self.arr_photo[self.num_photo])
        draw = ImageDraw.Draw(image)
        width = image.size[0]
        height = image.size[1]
        pix = image.load()
        for i in range(width):
            for j in range(height):
                a = pix[i, j][0]
                b = pix[i, j][1]
                c = pix[i, j][2]
                S = a + b + c
                if (S > (((255 + 100) // 2) * 3)):
                    a, b, c = 255, 255, 255
                else:
                    a, b, c = 0, 0, 0
                draw.point((i, j), (a, b, c))
        filePath, _ = QFileDialog.getSaveFileName(
            self, "Save", "", "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
        if filePath == "":
            return
        image.save(filePath)
        image.show()

    def Yarkosty(self):
        image = Image.open(self.arr_photo[self.num_photo])
        draw = ImageDraw.Draw(image)
        width = image.size[0]
        height = image.size[1]
        pix = image.load()
        o, okPressed = QInputDialog.getInt(
            self, "Уровень яркости", "Введите значение:", 0, -10000, 10000, 1)
        if okPressed:
            self.znach = o
        else:
            return
        for i in range(width):
            for j in range(height):
                a = pix[i, j][0] + self.znach
                b = pix[i, j][1] + self.znach
                c = pix[i, j][2] + self.znach
                draw.point((i, j), (a, b, c))
        filePath, _ = QFileDialog.getSaveFileName(
            self, "Save", "", "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
        if filePath == "":
            return
        image.save(filePath)
        image.show()

    def Matrita(self):
        self.window3 = MainClass()
        self.window3.show()

    def plus(self):
        img = QtWidgets.QFileDialog.getOpenFileName(
            self, "1 фото", "", "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")[0]
        if img == "":
            return
        image = Image.open(img)
        draw = ImageDraw.Draw(image)
        width = image.size[0]
        height = image.size[1]
        pix = image.load()

        img1 = QtWidgets.QFileDialog.getOpenFileName(
            self, "2 фото", "", "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")[0]
        if img1 == "":
            return
        image1 = Image.open(img1)
        draw1 = ImageDraw.Draw(image1)
        width1 = image1.size[0]
        height1 = image1.size[1]
        pix1 = image1.load()

        if(width == width1 and height == height1):
            for i in range(width):
                for j in range(height):
                    a = pix[i, j][0]
                    b = pix[i, j][1]
                    c = pix[i, j][2]
                    a1 = pix1[i, j][0]
                    b1 = pix1[i, j][1]
                    c1 = pix1[i, j][2]
                    suma = a + a1
                    sumb = b + b1
                    sumc = c + c1
                    if (suma > 255):
                        suma = 255
                    if (sumb > 255):
                        sumb = 255
                    if (sumb > 255):
                        sumb = 255
                    draw.point((i, j), (suma, sumb, sumc))
            filePath, _ = QFileDialog.getSaveFileName(
                self, "Save", "", "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
            if filePath == "":
                return
            image.save(filePath)
            image.show()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("ОШИБКА!")
            msg.setText("Размеры фотографий не совпадают!")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()

    def minus(self):
        img = QtWidgets.QFileDialog.getOpenFileName(
            self, "1 фото", "", "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")[0]
        if img == "":
            return
        image = Image.open(img)
        draw = ImageDraw.Draw(image)
        width = image.size[0]
        height = image.size[1]
        pix = image.load()

        img1 = QtWidgets.QFileDialog.getOpenFileName(
            self, "2 фото", "", "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")[0]
        if img1 == "":
            return
        image1 = Image.open(img1)
        draw1 = ImageDraw.Draw(image1)
        width1 = image1.size[0]
        height1 = image1.size[1]
        pix1 = image1.load()
        if(width == width1 and height == height1):
            for i in range(width):
                for j in range(height):
                    a = pix[i, j][0]
                    b = pix[i, j][1]
                    c = pix[i, j][2]
                    a1 = pix1[i, j][0]
                    b1 = pix1[i, j][1]
                    c1 = pix1[i, j][2]
                    suma = a - a1
                    sumb = b - b1
                    sumc = c - c1
                    if (suma < 0):
                        suma = 0
                    if (sumb < 0):
                        sumb = 0
                    if (sumb < 0):
                        sumb = 0
                    draw.point((i, j), (suma, sumb, sumc))
            filePath, _ = QFileDialog.getSaveFileName(
                self, "Save", "", "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
            if filePath == "":
                return
            image.save(filePath)
            image.show()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("ОШИБКА!")
            msg.setText("Размеры фотографий не совпадают!")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()

    def umnozenie(self):
        img = QtWidgets.QFileDialog.getOpenFileName(
            self, "1 фото", "", "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")[0]
        if img == "":
            return
        image = Image.open(img)
        draw = ImageDraw.Draw(image)
        width = image.size[0]
        height = image.size[1]
        pix = image.load()

        img1 = QtWidgets.QFileDialog.getOpenFileName(
            self, "2 фото", "", "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")[0]
        if img1 == "":
            return
        image1 = Image.open(img1)
        draw1 = ImageDraw.Draw(image1)
        width1 = image1.size[0]
        height1 = image1.size[1]
        pix1 = image1.load()
        if(width == width1 and height == height1):
            for i in range(width):
                for j in range(height):
                    a = pix[i, j][0]
                    b = pix[i, j][1]
                    c = pix[i, j][2]
                    a1 = pix1[i, j][0]
                    b1 = pix1[i, j][1]
                    c1 = pix1[i, j][2]
                    suma = a * a1
                    sumb = b * b1
                    sumc = c * c1
                    if (suma > 255):
                        suma = 255
                    if (sumb > 255):
                        sumb = 255
                    if (sumb > 255):
                        sumb = 255
                    draw.point((i, j), (suma, sumb, sumc))
            filePath, _ = QFileDialog.getSaveFileName(
                self, "Save", "", "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
            if filePath == "":
                return
            image.save(filePath)
            image.show()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("ОШИБКА!")
            msg.setText("Размеры фотографий не совпадают!")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()

    def delenie(self):
        img = QtWidgets.QFileDialog.getOpenFileName(
            self, "1 фото", "", "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")[0]
        if img == "":
            return
        image = Image.open(img)
        draw = ImageDraw.Draw(image)
        width = image.size[0]
        height = image.size[1]
        pix = image.load()

        img1 = QtWidgets.QFileDialog.getOpenFileName(
            self, "2 фото", "", "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")[0]
        if img1 == "":
            return
        image1 = Image.open(img1)
        draw1 = ImageDraw.Draw(image1)
        width1 = image1.size[0]
        height1 = image1.size[1]
        pix1 = image1.load()
        if(width == width1 and height == height1):
            for i in range(width):
                for j in range(height):
                    a = pix[i, j][0]
                    b = pix[i, j][1]
                    c = pix[i, j][2]
                    a1 = pix1[i, j][0]
                    b1 = pix1[i, j][1]
                    c1 = pix1[i, j][2]
                    suma = int(a / (a1+0.1))
                    sumb = int(b / (b1+0.1))
                    sumc = int(c / (c1+0.1))
                    draw.point((i, j), (suma, sumb, sumc))
            filePath, _ = QFileDialog.getSaveFileName(
                self, "Save", "", "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
            if filePath == "":
                return
            image.save(filePath)
            image.show()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("ОШИБКА!")
            msg.setText("Размеры фотографий не совпадают!")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()

    def vstavka(self):
        image = Image.open(self.arr_photo[self.num_photo])
        drawing = ImageDraw.Draw(image)
        black = (3, 8, 12)
        self.vibor = QtWidgets.QFileDialog.getOpenFileName(
            self, "Take", "", "otf(*otf)")[0]
        if self.vibor == "":
            return
        font = ImageFont.truetype(self.vibor, 41)
        a, okPressed = QInputDialog.getInt(
            self, "Координата а", "Введите значение:", 0, 0, 10000, 1)
        if okPressed:
            self.znach = a
        else:
            return
        b, okPressed = QInputDialog.getInt(
            self, "Координата b", "Введите значение:", 0, 0, 10000, 1)
        if okPressed:
            self.znach = b
        else:
            return
        pos = (a, b)
        slovo, okPressed = QInputDialog.getText(
            self, "Текст", "Введите текст:")
        if okPressed:
            self.znach = slovo
        else:
            return
        drawing.text(pos, slovo, fill=black, font=font)
        filePath, _ = QFileDialog.getSaveFileName(
            self, "Save", "", "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
        if filePath == "":
            return
        image.save(filePath)
        image.show()

    def rabota_s_shumami(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Выберите папку")
        self.num_photo = 0
        self.arr_photo = []
        extension = ['.png', '.jpeg.', '.jpg', '.bmp', '.gif']
        if directory:
            for file in os.listdir(directory):
                _, file_extension = os.path.splitext(file)
                if file_extension in extension:
                    self.arr_photo.append(directory + '/' + file)
        i, okPressed = QInputDialog.getInt(
            self, "Количество", "Введите значение:", 0, 0, 100, 1)
        if okPressed:
            self.znach = i
        else:
            return
        imgg = Image.open(self.arr_photo[0])
        width = imgg.size[0]
        height = imgg.size[1]

        imgg1 = Image.open(self.arr_photo[1])
        width1 = imgg1.size[0]
        height1 = imgg1.size[1]

        imgg2 = Image.open(self.arr_photo[2])
        width2 = imgg2.size[0]
        height2 = imgg2.size[1]

        if (width == width1 and height == height1):
            self.normaw = width
            self.normah = height
        if (width2 == width1 and height2 == height1):
            self.normaw = width2
            self.normah = height2
        if (width2 == width and height2 == height):
            self.normaw = width2
            self.normah = height2

        self.suma = np.zeros((width, height), dtype=int)
        self.sumb = np.zeros((width, height), dtype=int)
        self.sumc = np.zeros((width, height), dtype=int)

        while(self.num_photo <= i):
            imgg = Image.open(self.arr_photo[self.num_photo])
            draw = ImageDraw.Draw(imgg)
            width = imgg.size[0]
            height = imgg.size[1]
            pix = imgg.load()
            self.num_photo += 1

            if(width == self.normaw and height == self.normah):
                for k in range(width):
                    for m in range(height):
                        a = pix[k, m][0]
                        b = pix[k, m][1]
                        c = pix[k, m][2]
                        R1 = self.suma[k][m]
                        G1 = self.sumb[k][m]
                        B1 = self.sumc[k][m]
                        self.suma[k][m] = R1 + a
                        self.sumb[k][m] = G1 + b
                        self.sumc[k][m] = B1 + c

        for k in range(width):
            for m in range(height):
                self.suma[k][m] = int(self.suma[k][m]) // i
                self.sumb[k][m] = int(self.sumb[k][m]) // i
                self.sumc[k][m] = int(self.sumc[k][m]) // i
                draw.point(
                    (k, m), (self.suma[k][m], self.sumb[k][m], self.sumc[k][m]))
        filePath, _ = QFileDialog.getSaveFileName(
            self, "Save", "", "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
        if filePath == "":
            return
        imgg.save(filePath)
        imgg.show()


class MainClass(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainClass, self).__init__()
        self.ui = Matrita()
        self.ui.setupUi(self)
        self.show()
        self.ui.actionBrowse.triggered.connect(self.browse)
        self.ui.actionExit.triggered.connect(self.exit)
        self.ui.pushButton.clicked.connect(self.apply)
        self.ui.KarelitiaButton.setChecked(True)
        if imggggg != 0:
            print(imggggg)
            pixmap = QPixmap(imggggg)
            pixmap = pixmap.scaled(311, 321)
            self.ui.photo.setPixmap(pixmap)
            self.name = imggggg

    def browse(self):
        imgpath = QtWidgets.QFileDialog.getOpenFileName()[0]
        os.chdir(Path(imgpath).parent)
        self.name = Path(imgpath).name
        self.change(self.name)
        self.i(self.name)

    def exit(self):
        sys.exit()

    def change(self, name):
        self.ui.photo.setScaledContents(True)
        pixmap = QPixmap(self.name)
        self.ui.photo.setPixmap(pixmap)
        self.ui.statusbar.showMessage(self.name)
        self.i(self.name)

    def apply(self, name):
        str = self.ui.matrix.toPlainText()
        n = str.count("\n")+1
        cell = re.split("\n", str)
        m = cell[0].count(" ")+1
        cell = re.split("\n| ", str)
        matrix = np.zeros((n, m), dtype=np.int64)
        i = 0
        j = 0
        k = 0
        for i in range(n):
            for j in range(m):
                matrix[i][j] = cell[k]
                k += 1

        image = Image.open(self.name)
        image = ImageOps.expand(image, border=m, fill=0)

        width = image.size[0]
        height = image.size[1]
        pix = image.load()
        draw = ImageDraw.Draw(image)
        matrix0 = matrix
        if self.ui.KarelitiaButton.isChecked():
            matrix = matrix0
        if self.ui.SvrtkaButton.isChecked():
            matrix = np.rot90(np.rot90(matrix0))
        i = 0
        j = 0
        for i in range(width-n):
            for j in range(height-m):
                k = 0
                l = 0
                sr = 0
                sg = 0
                sb = 0
                for k in range(n):
                    for l in range(m):
                        r = pix[i+k, j+l][0] * matrix[k][l]
                        g = pix[i+k, j+l][1] * matrix[k][l]
                        b = pix[i+k, j+l][2] * matrix[k][l]
                        sr += r
                        sg += g
                        sb += b
                draw.point((i, j), (sr, sg, sb))
        image = ImageOps.crop(image, border=m)
        nazvanie, okPressed = QInputDialog.getText(
            self, "Название", "Введите имя фото:")
        if okPressed:
            ima = nazvanie
        else:
            return
        image.save(ima + ".png")
        top = ima + ".png"
        print(top)
        pixmap = QPixmap(top)
        self.ui.photo_2.setScaledContents(True)
        self.ui.photo_2.setPixmap(pixmap)

    def i(self, name):
        i = 0
        for i in range(len(os.listdir())):
            if (os.listdir()[i] == self.name):
                self.num = i


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Paint()
    window.show()
    app.exec()
