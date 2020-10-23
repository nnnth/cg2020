#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os
import math
from drawui import Ui_MainWindow
import numpy as np
from PIL import Image
import cg_algorithms as alg
from typing import Optional
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    qApp,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsItem,
    QListWidget,
    QHBoxLayout,
    QWidget,
    QStyleOptionGraphicsItem,
    QColorDialog,
    QDialog,
    QFormLayout,
    QLabel,
    QSpinBox,
    QDialogButtonBox,
    QFileDialog)
from PyQt5.QtGui import QPainter, QMouseEvent, QColor
from PyQt5.QtCore import QRectF, QPointF


def pointcmp(a, b, center):
    x0, y0 = a
    x1, y1 = b
    x, y = center
    if x0 >= center[0] > x1:
        return True
    if x0 == center[0] and x1 == center[0]:
        return y0 > y1
    det = (x0 - x) * (y1 - y) - (x1 - x) * (y0 - y)
    if det == 0:
        d1 = (x0 - x) * (x0 - x) + (y0 - y) * (y0 - y)
        d2 = (x1 - x) * (x1 - x) + (y1 - y) * (y1 - y)
        return d1 > d2
    else:
        return det < 0


class MyCanvas(QGraphicsView):
    """
    画布窗体类，继承自QGraphicsView，采用QGraphicsView、QGraphicsScene、QGraphicsItem的绘图框架
    """

    def __init__(self, *args):
        super().__init__(*args)
        self.main_window = None
        # self.list_widget = None
        self.item_dict = {}
        self.selected_id = ''

        self.status = ''
        self.temp_algorithm = ''
        self.temp_id = ''
        self.temp_item = None

    def start_draw(self, status, algorithm='', item_id=None):
        self.temp_item = None
        self.status = status
        self.temp_algorithm = algorithm
        if item_id:
            self.temp_id = item_id

    def finish_draw(self):
        self.temp_id = self.main_window.get_id()

    def start_select(self):
        self.status = ''

    def clear_selection(self):
        if self.selected_id != '':
            self.item_dict[self.selected_id].selected = False
            self.selected_id = ''

    def selection_changed(self, selected):
        self.main_window.statusBar().showMessage('图元选择： %s' % selected)
        if self.selected_id != '':
            self.item_dict[self.selected_id].selected = False
            self.item_dict[self.selected_id].update()
        self.selected_id = selected
        self.item_dict[selected].selected = True
        self.item_dict[selected].update()
        self.status = ''
        self.updateScene([self.sceneRect()])

    def redo(self):
        if self.temp_id != '':
            id = int(self.temp_id)
            while self.item_dict.get('%d' % id) is None:
                id = id - 1
            last_id = '%d' % id

            if len(self.item_dict[last_id].p_list) <= 2:
                self.scene().removeItem(self.item_dict[last_id])
                del self.item_dict[last_id]
            else:
                self.item_dict[last_id].p_list.pop()
            self.updateScene([self.sceneRect()])

    def mousePressEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.status == 'line' or self.status == 'ellipse':
            self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y]], self.temp_algorithm)
            self.scene().addItem(self.temp_item)
        elif self.status == 'polygon' or self.status == 'curve':
            if not self.temp_item or self.temp_item.item_type != self.status:
                self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y]], self.temp_algorithm)
                self.scene().addItem(self.temp_item)
            else:
                self.temp_item.p_list.append((x, y))
                self.temp_item.algorithm = self.temp_algorithm
            if self.status == 'polygon':
                self.temp_item.adjust()
        elif self.status in ['translate', 'rotate', 'scale']:
            self.temp_item = MyItem(self.temp_id, self.status, [x, y], self.temp_algorithm)
        elif self.status == 'clip':
            self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y]], self.temp_algorithm)
        else:
            for key, item in self.item_dict.items():
                if item.contains(x, y):
                    self.selection_changed(key)
                    break
        self.updateScene([self.sceneRect()])
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.status == 'line' or self.status == 'ellipse':
            self.temp_item.p_list[1] = [x, y]
        elif self.status == 'polygon' or self.status == 'curve':
            self.temp_item.p_list[-1] = [x, y]
            if self.status == 'polygon':
                self.temp_item.adjust()
        elif self.status == 'translate':
            item = self.item_dict[self.selected_id]
            self.item_dict[self.selected_id].p_list = alg.translate(item.p_list, x - self.temp_item.p_list[0],
                                                                    y - self.temp_item.p_list[1])
            self.temp_item.p_list = [x, y]
        elif self.status == 'rotate':
            item = self.item_dict[self.selected_id]
            rect = item.boundingRect()
            cx = rect.center().x()
            cy = rect.center().y()
            a = self.temp_item.p_list[0] - cx
            b = self.temp_item.p_list[1] - cy
            c = x - cx
            d = y - cy
            cos = (a * c + b * d) / (math.sqrt(a * a + b * b) * math.sqrt(c * c + d * d))
            r = math.acos(cos)
            if (a < 0 and y > self.temp_item.p_list[1]) or (a > 0 and y < self.temp_item.p_list[1]) or (
                    b < 0 and x < self.temp_item.p_list[0]) or (b > 0 and x > self.temp_item.p_list[0]):
                r = -r
            r = r * 180 / math.pi
            self.item_dict[self.selected_id].p_list = alg.rotate(item.p_list, cx, cy, r)
            self.temp_item.p_list = [x, y]
        elif self.status == 'scale':
            item = self.item_dict[self.selected_id]
            rect = item.boundingRect()
            cx = rect.center().x()
            cy = rect.center().y()
            width = rect.width()
            scale = abs((x - cx) / (width / 2))
            self.item_dict[self.selected_id].p_list = alg.scale(item.p_list, cx, cy, scale)
            self.temp_item.p_list = [x, y]
        self.updateScene([self.sceneRect()])
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if self.status in ['line', 'ellipse']:
            self.updateScene([self.sceneRect()])
            self.item_dict[self.temp_id] = self.temp_item
            # self.list_widget.addItem(self.temp_id)
            self.finish_draw()
        elif self.status in ['polygon', 'curve']:
            self.updateScene([self.sceneRect()])
            # if not self.item_dict.get(self.temp_id):
            #     self.list_widget.addItem(self.temp_id)
            if self.status == 'polygon':
                self.temp_item.adjust()
            self.item_dict[self.temp_id] = self.temp_item
        elif self.status == 'clip':
            pos = self.mapToScene(event.localPos().toPoint())
            x = int(pos.x())
            y = int(pos.y())
            item = self.item_dict[self.selected_id]
            self.temp_item.p_list[1] = (x, y)
            x_min = min(x, self.temp_item.p_list[0][0])
            x_max = max(x, self.temp_item.p_list[0][0])
            y_min = min(y, self.temp_item.p_list[0][1])
            y_max = max(y, self.temp_item.p_list[0][1])
            self.item_dict[self.selected_id].p_list = alg.clip(item.p_list, x_min, y_min, x_max, y_max,
                                                               self.temp_item.algorithm)
            self.updateScene([self.sceneRect()])

        super().mouseReleaseEvent(event)

    def save_scene(self):
        save_name, _ = QFileDialog.getSaveFileName(self, 'Save Picture', '../imgs', 'Files (*.bmp)')
        canvas = np.zeros([self.height(), self.width(), 3], np.uint8)
        canvas.fill(255)
        for item in self.item_dict.values():
            item_type = item.item_type
            p_list = item.p_list
            algorithm = item.algorithm
            color = [item.color.red(), item.color.green(), item.color.black()]
            if item_type == 'line':
                pixels = alg.draw_line(p_list, algorithm)
            elif item_type == 'polygon':
                pixels = alg.draw_polygon(p_list, algorithm)
            elif item_type == 'ellipse':
                pixels = alg.draw_ellipse(p_list)
            elif item_type == 'curve':
                pixels = alg.draw_curve(p_list, algorithm)
            for x, y in pixels:
                canvas[y, x] = color

        Image.fromarray(canvas).save(os.path.join(save_name + '.bmp'), 'bmp')


class MyItem(QGraphicsItem):
    """
    自定义图元类，继承自QGraphicsItem
    """
    _color = QColor()

    def __init__(self, item_id: str, item_type: str, p_list: list, algorithm: str = '', parent: QGraphicsItem = None):
        """

        :param item_id: 图元ID
        :param item_type: 图元类型，'line'、'polygon'、'ellipse'、'curve'等
        :param p_list: 图元参数
        :param algorithm: 绘制算法，'DDA'、'Bresenham'、'Bezier'、'B-spline'等
        :param parent:
        """
        super().__init__(parent)
        self.id = item_id  # 图元ID
        self.item_type = item_type  # 图元类型，'line'、'polygon'、'ellipse'、'curve'等
        self.p_list = p_list  # 图元参数
        self.algorithm = algorithm  # 绘制算法，'DDA'、'Bresenham'、'Bezier'、'B-spline'等
        self.selected = False
        self.color = self._color
        self.fill_color = QColor(255, 255, 255)
        self.isfill = False

    @classmethod
    def set_color(cls, color):
        cls._color = color

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: Optional[QWidget] = ...) -> None:
        painter.setPen(self.color)
        if self.item_type == 'line':
            item_pixels = alg.draw_line(self.p_list, self.algorithm)
            for p in item_pixels:
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())
        elif self.item_type == 'polygon':
            item_pixels = alg.draw_polygon(self.p_list, self.algorithm)
            if self.isfill:
                self.fill(painter, self.fill_color)
            for p in item_pixels:
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())
        elif self.item_type == 'ellipse':
            item_pixels = alg.draw_ellipse(self.p_list)
            for p in item_pixels:
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())
        elif self.item_type == 'curve':
            item_pixels = alg.draw_curve(self.p_list[:], self.algorithm)
            for p in item_pixels:
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())

    def boundingRect(self) -> QRectF:
        x0, x1, y0, y1 = 20000, 0, 20000, 0
        for x, y in self.p_list:
            if x < x0:
                x0 = x
            if x > x1:
                x1 = x
            if y < y0:
                y0 = y
            if y > y1:
                y1 = y
        w = x1 - x0
        h = y1 - y0
        return QRectF(x0 - 1, y0 - 1, w + 2, h + 2)

    def adjust(self):
        cx = 0
        cy = 0
        for x, y in self.p_list:
            cx = cx + x
            cy = cy + y
        cx = cx / len(self.p_list)
        cy = cy / len(self.p_list)
        for i in range(len(self.p_list)):
            for j in range(len(self.p_list) - i - 1):
                if pointcmp(self.p_list[j], self.p_list[j + 1], [cx, cy]):
                    self.p_list[j], self.p_list[j + 1] = self.p_list[j + 1], self.p_list[j]

    def contains(self, x, y):
        if self.item_type == 'line':
            x0, y0 = self.p_list[0]
            x1, y1 = self.p_list[1]
            linewidth = 15
            if (y > y0 + linewidth and y > y1 + linewidth) or (y < y0 - linewidth and y < y1 - linewidth) or (
                    x > x0 + linewidth and x > x1 + linewidth) or (x < x0 - linewidth and x < x1 - linewidth):
                return False
            if x0 == x1:
                return abs(x - x0) < linewidth
            k = (y1 - y0) / (x1 - x0)
            b = (x1 * y0 - y1 * x0) / (x1 - x0)
            distance = pow(k * x - y + b, 2) / (pow(k, 2) + pow(b, 2))
            return distance < pow(linewidth, 2)
        elif self.item_type == 'ellipse':
            x0, y0 = self.p_list[0]
            x1, y1 = self.p_list[1]
            midx = (x0 + x1) / 2
            midy = (y0 + y1) / 2
            a = abs(x0 - x1) / 2
            b = abs(y0 - y1) / 2
            # if a == 0 or b == 0:
            #     return False
            print((pow(x - midx, 2) / pow(a, 2) + pow(y - midy, 2) / pow(b, 2)))
            return (pow(x - midx, 2) / pow(a, 2) + pow(y - midy, 2) / pow(b, 2)) <= 1
        else:
            return self.boundingRect().contains(x, y)

    def fill(self, painter, color):
        painter.setPen(color)
        if self.item_type == 'polygon' and len(self.p_list) > 2:
            NET = {}
            ymin = 1000
            ymax = 0
            for i in range(-1, len(self.p_list) - 1):
                x0, y0 = self.p_list[i]
                x1, y1 = self.p_list[i + 1]
                ymin = min([ymin, y0, y1])
                ymax = max([ymax, y0, y1])
                dx = 0
                if y0 != y1:
                    dx = (x0 - x1) / (y0 - y1)
                else:
                    continue
                if y1 > y0:
                    startx = x0
                else:
                    startx = x1
                if NET.get(min(y0, y1)) is None:
                    NET[min(y0, y1)] = [[startx, dx, max(y0, y1)]]
                else:
                    NET[min(y0, y1)].append([startx, dx, max(y0, y1)])

            AET = []
            for i in range(ymin, ymax):
                if NET.get(i):
                    AET.extend(NET.get(i))
                AET.sort(key=lambda x: x[0])
                for j in range(len(AET) - 1, -1, -1):
                    if AET[j][2] == i:
                        AET.remove(AET[j])
                    elif AET[j][2] > i:
                        AET[j][0] = AET[j][0] + AET[j][1]
                for k in range(len(AET) - 1):
                    pixels = alg.draw_line([(round(AET[k][0]), i), (round(AET[k + 1][0]), i)], 'DDA')
                    for p in pixels:
                        painter.drawPoint(*p)


class MainWindow(QMainWindow,Ui_MainWindow):
    """
    主窗口类
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.item_cnt = 0
        self.default_alg = ['Bresenham', 'Bezier', 'liang_barsky']
        self.fill_color = QColor(255, 255, 255)

        # 使用QListWidget来记录已有的图元，并用于选择图元。注：这是图元选择的简单实现方法，更好的实现是在画布中直接用鼠标选择图元
        # self.list_widget = QListWidget(self)
        # self.list_widget.setMinimumWidth(200)
        # self.list_widget.setGeometry(640, 160, 100, 420)

        # 使用QGraphicsView作为画布
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 600, 600)
        self.canvas_widget = MyCanvas(self.scene, self.centralWidget())
        self.canvas_widget.setFixedSize(600, 600)
        self.canvas_widget.main_window = self
        # self.canvas_widget.list_widget = self.list_widget

        self.action_DDA.triggered.connect(self.line_dda_action)
        self.action_click.triggered.connect(self.canvas_widget.start_select)
        self.actionellipse.triggered.connect(self.ellipse_action)
        self.action_Bresenham.triggered.connect(self.line_Bresenham_action)
        self.action_DDA_2.triggered.connect(self.polygon_dda_action)
        self.action_Bresenham_2.triggered.connect(self.polygon_Bresenham_action)
        self.action_Bezier.triggered.connect(self.curve_bezier_action)
        self.action_B_spline.triggered.connect(self.curve_b_spline_action)
        self.action_redo.triggered.connect(self.canvas_widget.redo)
        self.action_move.triggered.connect(self.translate_action)
        self.action_rotate.triggered.connect(self.rotate_action)
        self.action_scale.triggered.connect(self.scale_action)
        self.actioncohen_sutherland.triggered.connect(self.clip_cohen_sutherland_action)
        self.actionliang_barsky_action.triggered.connect(self.clip_liang_barsky_action)
        self.action_line2.triggered.connect(self.line_action)
        self.action_polygon2.triggered.connect(self.polygon_action)
        self.action_ellipse2.triggered.connect(self.ellipse_action)
        self.action_curve2.triggered.connect(self.curve_action)
        self.action_move2.triggered.connect(self.translate_action)
        self.action_rotate2.triggered.connect(self.rotate_action)
        self.action_scale2.triggered.connect(self.scale_action)
        self.action_clip2.triggered.connect(self.clip_action)
        self.action_pen.triggered.connect(self.get_color)
        self.action_fill.triggered.connect(self.fill_action)
        self.action1.triggered.connect(self.reset)
        self.action2.triggered.connect(self.canvas_widget.save_scene)
        self.pushButton.clicked.connect(self.get_color)
        self.pushButton_2.clicked.connect(self.set_fill_color)
        self.pushButton.setStyleSheet(
            'background-color:rgb({},{},{});'.format(self.fill_color.red(), self.fill_color.green(),
                                                     self.fill_color.blue()))
        self.pushButton_2.setStyleSheet(
            'background-color:rgb({},{},{});'.format(self.fill_color.red(), self.fill_color.green(),
                                                     self.fill_color.blue()))


    def set_fill_color(self):
        self.fill_color = QColorDialog.getColor()
        self.pushButton_2.setStyleSheet(
            'background-color:rgb({},{},{});'.format(self.fill_color.red(), self.fill_color.green(),
                                                     self.fill_color.blue()))

    def get_id(self):
        _id = str(self.item_cnt)
        self.item_cnt += 1
        return _id

    def get_color(self):
        color = QColorDialog.getColor()
        MyItem.set_color(color)
        self.pushButton.setStyleSheet(
            'background-color:rgb({},{},{});'.format(color.red(), color.green(),
                                                     color.blue()))

    def resetCanvas(self, x, y):
        # self.canvas_widget.list_widget.clear()
        self.canvas_widget.item_dict = {}
        self.canvas_widget.status = ''
        self.canvas_widget.selected_id = ''
        self.canvas_widget.setFixedSize(x, y)
        self.canvas_widget.setSceneRect(0, 0, x, y)
        self.item_cnt = 0
        self.canvas_widget.scene().clear()

    def reset(self):
        dialog = QDialog(self)
        form = QFormLayout(dialog)
        form.addRow(QLabel("User input:"))
        # width
        spinbox1 = QSpinBox(dialog)
        spinbox1.setMinimum(100)
        spinbox1.setMaximum(1000)
        form.addRow('width:', spinbox1)
        # height
        spinbox2 = QSpinBox(dialog)
        spinbox2.setMinimum(100)
        spinbox2.setMaximum(1000)
        form.addRow('height:', spinbox2)
        buttonbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, dialog)
        form.addRow(buttonbox)

        def set():
            x = int(spinbox1.text())
            y = int(spinbox2.text())
            print(x, y)
            self.resetCanvas(x, y)
            dialog.close()

        buttonbox.accepted.connect(set)
        buttonbox.rejected.connect(dialog.close)
        dialog.show()

    def fill_action(self):
        id = self.canvas_widget.selected_id
        if id and self.canvas_widget.item_dict[id].item_type == 'polygon':
            self.canvas_widget.item_dict[id].isfill = True
            self.canvas_widget.item_dict[id].fill_color = self.fill_color
            self.scene.update()

    def line_action(self):
        if self.default_alg[0] == 'DDA':
            self.line_dda_action()
        else:
            self.line_Bresenham_action()

    def line_naive_action(self):
        self.canvas_widget.start_draw('line', 'Naive', self.get_id())
        self.statusBar().showMessage('Naive算法绘制线段')
        # self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def line_dda_action(self):
        self.default_alg[0] = 'DDA'
        self.canvas_widget.start_draw('line', 'middle', self.get_id())
        self.statusBar().showMessage('middle算法绘制线段')
        # self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def line_Bresenham_action(self):
        self.default_alg[0] = 'Bresenham'
        self.canvas_widget.start_draw('line', 'Bresenham', self.get_id())
        self.statusBar().showMessage('Bresenham算法绘制线段')
        # self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def polygon_action(self):
        if self.default_alg[0] == 'DDA':
            self.polygon_dda_action()
        else:
            self.polygon_Bresenham_action()

    def polygon_dda_action(self):
        self.default_alg[0] = 'DDA'
        self.canvas_widget.start_draw('polygon', 'DDA', self.get_id())
        self.statusBar().showMessage('DDA算法绘制多边形')
        # self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def polygon_Bresenham_action(self):
        self.default_alg[0] = 'Bresenham'
        self.canvas_widget.start_draw('polygon', 'Bresenham', self.get_id())
        self.statusBar().showMessage('Bresenham算法绘制多边形')
        # self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def ellipse_action(self):
        self.canvas_widget.start_draw('ellipse', '中点圆生成算法', self.get_id())
        self.statusBar().showMessage('中点圆生成算法绘制椭圆')
        # self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def curve_action(self):
        if self.default_alg[1] == 'Bezier':
            self.curve_bezier_action()
        else:
            self.curve_b_spline_action()

    def curve_bezier_action(self):
        self.default_alg[1] = 'Bezier'
        self.canvas_widget.start_draw('curve', 'Bezier', self.get_id())
        self.statusBar().showMessage('Bezier绘制曲线')
        # self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def curve_b_spline_action(self):
        self.default_alg[1] = 'b_spline'
        self.canvas_widget.start_draw('curve', 'b_spline', self.get_id())
        self.statusBar().showMessage('三次均匀B样条绘制曲线')
        # self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def translate_action(self):
        self.canvas_widget.start_draw('translate', '')
        self.statusBar().showMessage('平移变换')

    def rotate_action(self):
        self.canvas_widget.start_draw('rotate', '')
        self.statusBar().showMessage('旋转变换（除椭圆外）')

    def scale_action(self):
        self.canvas_widget.start_draw('scale', '')
        self.statusBar().showMessage('缩放变换')

    def clip_action(self):
        if self.default_alg[2] == 'liang_barsky':
            self.clip_liang_barsky_action()
        else:
            self.clip_cohen_sutherland_action()

    def clip_cohen_sutherland_action(self):
        self.default_alg[2] = 'Cohen-Sutherland'
        self.canvas_widget.start_draw('clip', 'Cohen-Sutherland')
        self.statusBar().showMessage('Cohen-Sutherland算法线段裁剪')

    def clip_liang_barsky_action(self):
        self.default_alg[2] = 'liang_barsky'
        self.canvas_widget.start_draw('clip', 'liang_barsky')
        self.statusBar().showMessage('liang_barsky算法线段裁剪')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
