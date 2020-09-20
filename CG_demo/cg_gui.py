#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import math
import cg_algorithms as alg
from typing import Optional
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
    QDialogButtonBox)
from PyQt5.QtGui import QPainter, QMouseEvent, QColor
from PyQt5.QtCore import QRectF, QPointF


class MyCanvas(QGraphicsView):
    """
    画布窗体类，继承自QGraphicsView，采用QGraphicsView、QGraphicsScene、QGraphicsItem的绘图框架
    """

    def __init__(self, *args):
        super().__init__(*args)
        self.main_window = None
        self.list_widget = None
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
        elif self.status in ['translate', 'rotate', 'scale']:
            self.temp_item = MyItem(self.temp_id, self.status, [x, y], self.temp_algorithm)
        elif self.status == 'clip':
            self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y]], self.temp_algorithm)
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
            self.item_dict[self.selected_id].p_list = alg.rotate(item.p_list, cx, cy, r)
            self.temp_item.p_list = [x, y]
        elif self.status == 'scale':
            item = self.item_dict[self.selected_id]
            rect = item.boundingRect()
            cx = rect.center().x()
            cy = rect.center().y()
            width = rect.width()
            scale = abs((x - cx) / (width / 2))
            print(item.p_list)
            self.item_dict[self.selected_id].p_list = alg.scale(item.p_list, cx, cy, scale)
            self.temp_item.p_list = [x, y]
        self.updateScene([self.sceneRect()])
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if self.status in ['line', 'ellipse']:
            self.updateScene([self.sceneRect()])
            self.item_dict[self.temp_id] = self.temp_item
            self.list_widget.addItem(self.temp_id)
            self.finish_draw()
        elif self.status in ['polygon', 'curve']:
            self.updateScene([self.sceneRect()])
            if not self.item_dict.get(self.temp_id):
                self.list_widget.addItem(self.temp_id)
            self.item_dict[self.temp_id] = self.temp_item
            'self.finish_draw()'
        elif self.status == 'clip':
            pos = self.mapToScene(event.localPos().toPoint())
            x = int(pos.x())
            y = int(pos.y())
            item = self.item_dict[self.selected_id]
            self.temp_item.p_list[1] = (x,y)
            x_min = min(x,self.temp_item.p_list[0][0])
            x_max = max(x,self.temp_item.p_list[0][0])
            y_min = min(y,self.temp_item.p_list[0][1])
            y_max = max(y,self.temp_item.p_list[0][1])
            self.item_dict[self.selected_id].p_list = alg.clip(item.p_list,x_min,y_min,x_max,y_max,self.temp_item.algorithm)
            print(self.item_dict[self.selected_id].p_list)
            self.updateScene([self.sceneRect()])

        super().mouseReleaseEvent(event)


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
            item_pixels = alg.draw_curve(self.p_list, self.algorithm)
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


class MainWindow(QMainWindow):
    """
    主窗口类
    """

    def __init__(self):
        super().__init__()
        self.item_cnt = 0

        # 使用QListWidget来记录已有的图元，并用于选择图元。注：这是图元选择的简单实现方法，更好的实现是在画布中直接用鼠标选择图元
        self.list_widget = QListWidget(self)
        self.list_widget.setMinimumWidth(200)

        # 使用QGraphicsView作为画布
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 600, 600)
        self.canvas_widget = MyCanvas(self.scene, self)
        self.canvas_widget.setFixedSize(600, 600)
        self.canvas_widget.main_window = self
        self.canvas_widget.list_widget = self.list_widget

        # 设置菜单栏
        menubar = self.menuBar()
        file_menu = menubar.addMenu('文件')
        set_pen_act = file_menu.addAction('设置画笔')
        reset_canvas_act = file_menu.addAction('重置画布')
        exit_act = file_menu.addAction('退出')
        draw_menu = menubar.addMenu('绘制')
        line_menu = draw_menu.addMenu('线段')
        line_naive_act = line_menu.addAction('Naive')
        line_dda_act = line_menu.addAction('DDA')
        line_bresenham_act = line_menu.addAction('Bresenham')
        polygon_menu = draw_menu.addMenu('多边形')
        polygon_dda_act = polygon_menu.addAction('DDA')
        polygon_bresenham_act = polygon_menu.addAction('Bresenham')
        ellipse_act = draw_menu.addAction('椭圆')
        curve_menu = draw_menu.addMenu('曲线')
        curve_bezier_act = curve_menu.addAction('Bezier')
        curve_b_spline_act = curve_menu.addAction('B-spline')
        edit_menu = menubar.addMenu('编辑')
        translate_act = edit_menu.addAction('平移')
        rotate_act = edit_menu.addAction('旋转')
        scale_act = edit_menu.addAction('缩放')
        clip_menu = edit_menu.addMenu('裁剪')
        clip_cohen_sutherland_act = clip_menu.addAction('Cohen-Sutherland')
        clip_liang_barsky_act = clip_menu.addAction('Liang-Barsky')

        # 连接信号和槽函数-set_pen
        set_pen_act.triggered.connect(self.get_color)
        reset_canvas_act.triggered.connect(self.reset)
        self.list_widget.currentTextChanged.connect(self.canvas_widget.selection_changed)
        exit_act.triggered.connect(qApp.quit)
        line_naive_act.triggered.connect(self.line_naive_action)
        line_dda_act.triggered.connect(self.line_dda_action)
        line_bresenham_act.triggered.connect(self.line_Bresenham_action)
        polygon_dda_act.triggered.connect(self.polygon_dda_action)
        polygon_bresenham_act.triggered.connect(self.polygon_Bresenham_action)
        ellipse_act.triggered.connect(self.ellipse_action)
        curve_bezier_act.triggered.connect(self.curve_bezier_action)
        curve_b_spline_act.triggered.connect(self.curve_b_spline_action)
        translate_act.triggered.connect(self.translate_action)
        rotate_act.triggered.connect(self.rotate_action)
        scale_act.triggered.connect(self.scale_action)
        clip_cohen_sutherland_act.triggered.connect(self.clip_cohen_sutherland_action)
        clip_liang_barsky_act.triggered.connect(self.clip_liang_barsky_action)

        # 设置主窗口的布局
        self.hbox_layout = QHBoxLayout()
        self.hbox_layout.addWidget(self.canvas_widget)
        self.hbox_layout.addWidget(self.list_widget, stretch=1)
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.hbox_layout)
        self.setCentralWidget(self.central_widget)
        self.statusBar().showMessage('空闲')
        self.resize(600, 600)
        self.setWindowTitle('CG Demo')

    def get_id(self):
        _id = str(self.item_cnt)
        self.item_cnt += 1
        return _id

    def get_color(self):
        color = QColorDialog.getColor()
        MyItem.set_color(color)

    def resetCanvas(self, x, y):
        self.canvas_widget.list_widget.clear()
        self.canvas_widget.item_dict = {}
        self.canvas_widget.status = ''
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

    def line_naive_action(self):
        self.canvas_widget.start_draw('line', 'Naive', self.get_id())
        self.statusBar().showMessage('Naive算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def line_dda_action(self):
        self.canvas_widget.start_draw('line', 'DDA', self.get_id())
        self.statusBar().showMessage('DDA算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def line_Bresenham_action(self):
        self.canvas_widget.start_draw('line', 'Bresenham', self.get_id())
        self.statusBar().showMessage('Bresenham算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def polygon_dda_action(self):
        self.canvas_widget.start_draw('polygon', 'DDA', self.get_id())
        self.statusBar().showMessage('DDA算法绘制多边形')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def polygon_Bresenham_action(self):
        self.canvas_widget.start_draw('polygon', 'Bresenham', self.get_id())
        self.statusBar().showMessage('Bresenham算法绘制多边形')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def ellipse_action(self):
        self.canvas_widget.start_draw('ellipse', '中点圆生成算法', self.get_id())
        self.statusBar().showMessage('中点圆生成算法绘制椭圆')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def curve_bezier_action(self):
        self.canvas_widget.start_draw('curve', 'Bezier', self.get_id())
        self.statusBar().showMessage('Bezier绘制曲线')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def curve_b_spline_action(self):
        self.canvas_widget.start_draw('curve', 'b_spline', self.get_id())
        self.statusBar().showMessage('三次均匀B样条绘制曲线')
        self.list_widget.clearSelection()
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

    def clip_cohen_sutherland_action(self):
        self.canvas_widget.start_draw('clip', 'Cohen-Sutherland')
        self.statusBar().showMessage('Cohen-Sutherland算法线段裁剪')

    def clip_liang_barsky_action(self):
        self.canvas_widget.start_draw('clip', 'liang_barsky')
        self.statusBar().showMessage('liang_barsky算法线段裁剪')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
