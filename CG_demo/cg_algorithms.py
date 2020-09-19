#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 本文件只允许依赖math库
import math


def draw_line(p_list, algorithm):
    """绘制线段

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 线段的起点和终点坐标
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'，此处的'Naive'仅作为示例，测试时不会出现
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    result = []
    if algorithm == 'Naive':
        if x0 == x1:
            for y in range(y0, y1 + 1):
                result.append((x0, y))
        else:
            if x0 > x1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            k = (y1 - y0) / (x1 - x0)
            for x in range(x0, x1 + 1):
                result.append((x, int(y0 + k * (x - x0))))
    elif algorithm == 'DDA':
        lenx = x1 - x0
        leny = y1 - y0
        if abs(lenx) >= abs(leny):
            length = abs(lenx)
        else:
            length = abs(leny)
        if length == 0:
            result = [(int(x0), int(y0))]
            return result
        deltax = lenx / length
        deltay = leny / length
        result.append((x0, y0))
        for i in range(length):
            x0 = x0 + deltax
            y0 = y0 + deltay
            result.append((int(x0), int(y0)))
    elif algorithm == 'Bresenham':
        lenx = abs(x1 - x0)
        leny = abs(y1 - y0)
        reverse = False
        if lenx >= leny:
            dx = lenx
            dy = leny
        else:
            dx = leny
            dy = lenx
            reverse = True
        p = 2 * dy - dx
        stepx = 1 if x1 > x0 else -1
        stepy = 1 if y1 > y0 else -1
        result.append((x0, y0))
        for i in range(dx):
            if reverse:
                x0 = x0 + (p >= 0) * stepx
                y0 = y0 + stepy
            else:
                x0 = x0 + stepx
                y0 = y0 + (p >= 0) * stepy
            p = p + 2 * dy - 2 * (p >= 0) * dx
            result.append((x0, y0))
    return result


def draw_polygon(p_list, algorithm):
    """绘制多边形

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 多边形的顶点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    for i in range(len(p_list)):
        line = draw_line([p_list[i - 1], p_list[i]], algorithm)
        result += line
    return result


def draw_ellipse(p_list):
    """绘制椭圆（采用中点圆生成算法）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 椭圆的矩形包围框左上角和右下角顶点坐标
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    if x0 == x1 and y0 == y1:
        result.append((x0, y0))
        return result
    a = (max(x0, x1) - min(x0, x1)) / 2
    b = (max(y0, y1) - min(y0, y1)) / 2
    reverse = False
    mid = [(x0 + x1) / 2, (y0 + y1) / 2]
    if a < b:
        reverse = True
        a, b = b, a
    p = b * b - a * a * b + a * a / 4
    x = 0
    y = b
    if reverse:
        result.append((y, x))
    else:
        result.append((x, y))
    b_square = b * b
    a_square = a * a
    while b_square * x < a_square * y:
        if p < 0:
            p = p + 2 * b_square * x + 3 * b_square
            x = x + 1
            if reverse:
                result.append((y, x))
            else:
                result.append((x, y))
        else:
            p = p + 2 * b_square * x - 2 * a_square * y + 2 * a_square + 3 * b_square
            x = x + 1
            y = y - 1
            if reverse:
                result.append((y, x))
            else:
                result.append((x, y))

    p = b_square * (x + 0.5) * (x + 0.5) + a_square * (y - 1) * (y - 1) - a_square * b_square
    while y >= 0:
        if p > 0:
            p = p - 2 * a_square * y + 3 * a_square
            y = y - 1
            if reverse:
                result.append((y, x))
            else:
                result.append((x, y))

        else:
            p = p + 2 * b_square * x - 2 * a_square * y + 2 * b_square + 3 * a_square
            x = x + 1
            y = y - 1
            if reverse:
                result.append((y, x))
            else:
                result.append((x, y))
    temp = result
    for x, y in temp[:]:
        result.append((-x, -y))
        result.append((-x, y))
        result.append((x, -y))
    for i in range(len(result)):
        result[i] = (result[i][0] + mid[0], result[i][1] + mid[1])
    return result


def draw_curve(p_list, algorithm):
    """绘制曲线

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 曲线的控制点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'Bezier'和'B-spline'（三次均匀B样条曲线，曲线不必经过首末控制点）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    p_list.sort(key=lambda a: a[0])
    n = len(p_list) - 1
    if algorithm == 'Bezier' or n<3:
        u = 0
        while u < 1:
            temp = p_list[:]
            for r in range(n):
                for i in range(n - r):
                    temp[i] = [(1 - u) * temp[i][0] + u * temp[i + 1][0], (1 - u) * temp[i][1] + u * temp[i + 1][1]]
            u = u + 0.002
            result.append((round(temp[0][0]), round(temp[0][1])))
    else:
        for i in range(n - 2):
            u = 0
            while u <= 1:
                u_2 = pow(u, 2)
                u_3 = pow(u, 3)
                x = 1 / 6 * (
                            (-u_3 + 3 * u_2 - 3 * u + 1) * p_list[i][0] + (3 * u_3 - 6 * u_2 + 4) * p_list[i + 1][0] + (
                                -3 * u_3 + 3 * u_2 + 3 * u + 1) * p_list[i + 2][0] + u_3 * p_list[i + 3][0])
                y = 1 / 6 * (
                            (-u_3 + 3 * u_2 - 3 * u + 1) * p_list[i][1] + (3 * u_3 - 6 * u_2 + 4) * p_list[i + 1][1] + (
                                -3 * u_3 + 3 * u_2 + 3 * u + 1) * p_list[i + 2][1] + u_3 * p_list[i + 3][1])
                result.append((round(x), round(y)))
                u = u + 0.01
    return result


def translate(p_list, dx, dy):
    """平移变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param dx: (int) 水平方向平移量
    :param dy: (int) 垂直方向平移量
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    result = []
    for x,y in p_list[:]:
        result.append((x+dx,y+dy))
    return result


def rotate(p_list, x, y, r):
    """旋转变换（除椭圆外）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 旋转中心x坐标
    :param y: (int) 旋转中心y坐标
    :param r: (int) 顺时针旋转角度（°）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    pass


def scale(p_list, x, y, s):
    """缩放变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 缩放中心x坐标
    :param y: (int) 缩放中心y坐标
    :param s: (float) 缩放倍数
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    pass


def clip(p_list, x_min, y_min, x_max, y_max, algorithm):
    """线段裁剪

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 线段的起点和终点坐标
    :param x_min: 裁剪窗口左上角x坐标
    :param y_min: 裁剪窗口左上角y坐标
    :param x_max: 裁剪窗口右下角x坐标
    :param y_max: 裁剪窗口右下角y坐标
    :param algorithm: (string) 使用的裁剪算法，包括'Cohen-Sutherland'和'Liang-Barsky'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1]]) 裁剪后线段的起点和终点坐标
    """
    pass


if __name__ == '__main__':
    print(range(0, 1, 0.01))
