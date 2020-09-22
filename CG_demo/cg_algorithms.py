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
    if not p_list:
        return []
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
            result.append((round(x0), round(y0)))
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
    mid = [int((x0 + x1) / 2), int((y0 + y1) / 2)]
    if a < b:
        reverse = True
        a, b = b, a
    p = b * b - a * a * b + a * a / 4
    x = 0
    y = int(b)
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
    if algorithm == 'Bezier':
        u = 0
        while u < 1:
            temp = p_list[:]
            for r in range(n):
                for i in range(n - r):
                    temp[i] = [(1 - u) * temp[i][0] + u * temp[i + 1][0], (1 - u) * temp[i][1] + u * temp[i + 1][1]]
            u = u + 0.002
            result.append((round(temp[0][0]), round(temp[0][1])))
    else:
        # print(n)
        # delta = 1 / (n + 4)
        # u = [0]
        # for i in range(1, n + 4):
        #     u.append(u[i - 1] + delta)
        # u.append(1)
        # print(u)
        # t = u[3]
        # j = 3
        # while t <= u[n + 1]:
        #     temp = p_list[:]
        #     j = int(t/ delta)
        #     for r in range(1,4):
        #         for i in range(j - 4 + r + 1, j + 1):
        #             try:
        #                 lam = (t - u[i]) / (u[i + 4 - r] - u[i])
        #                 temp[j] = [lam * temp[j][0] + (1 - lam) * temp[j - 1][0],
        #                            lam * temp[j][1] + (1 - lam) * temp[j - 1][1]]
        #             except Exception:
        #                 print(i,j,r)
        #                 exit()
        #     t = t + 0.002
        #     result.append((round(temp[j][0]), round(temp[j][1])))
        if n == 0:
            return p_list
        elif n == 1:
            return draw_line(p_list, 'DDA')
        elif n == 2:
            u = 0
            while u <= 1:
                u_2 = pow(u, 2)
                x = 1/2*((u_2 - 2 * u + 1) * p_list[0][0] + (- 2 * u_2 + 2 * u+1) * p_list[1][0] + u_2 * p_list[2][
                    0])
                y = 1/2*((u_2 - 2 * u + 1) * p_list[0][1] + (- 2 * u_2 + 2 * u+1) * p_list[1][1] + u_2 * p_list[2][
                    1])
                result.append((round(x), round(y)))
                u = u + 0.001
            return result
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
    for x, y in p_list[:]:
        result.append((x + dx, y + dy))
    return result


def rotate(p_list, x, y, r):
    """旋转变换（除椭圆外）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 旋转中心x坐标
    :param y: (int) 旋转中心y坐标
    :param r: (int) 顺时针旋转角度（°）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    'P=((Xo-Cx)×cosθ-(Yo-Cy)×sinθ+Cx,(Xo-Cx)×sinθ+(Yo-Cy)×cosθ+Cy)'
    r = (r / 180) * math.pi
    result = []
    for a, b in p_list:
        a1 = (a - x) * math.cos(r) - (b - y) * math.sin(r) + x
        b1 = (a - x) * math.sin(r) + (b - y) * math.cos(r) + y
        result.append((round(a1), round(b1)))
    return result


def scale(p_list, x, y, s):
    """缩放变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 缩放中心x坐标
    :param y: (int) 缩放中心y坐标
    :param s: (float) 缩放倍数
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    result = []
    for a, b in p_list:
        a = (a - x) * s + x
        b = (b - y) * s + y
        result.append((round(a), round(b)))
    return result


def test(p, q, u1, u2):
    if p < 0:
        u1 = max(u1, q / p)
    elif p > 0:
        u2 = min(u2, q / p)
    elif q < 0:
        return False, 0, 0
    return u1 <= u2, u1, u2


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
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    if algorithm == 'Cohen-Sutherland':
        while True:
            code1 = (y0 > y_max) << 3 | (y0 < y_min) << 2 | (x0 > x_max) << 1 | (x0 < x_min)
            code2 = (y1 > y_max) << 3 | (y1 < y_min) << 2 | (x1 > x_max) << 1 | (x1 < x_min)
            if code1 | code2 == 0:
                return [(x0, y0), (x1, y1)]
            if code1 & code2 != 0:
                return []
            if code1 == 0:
                x0, y0, x1, y1 = x1, y1, x0, y0
            if code1 & 0x8 == 8:
                u = (y_max - y0) / (y1 - y0)
                x0 = round(x0 + u * (x1 - x0))
                y0 = y_max
            elif code1 & 0x4 == 4:
                u = (y_min - y0) / (y1 - y0)
                x0 = round(x0 + u * (x1 - x0))
                y0 = y_min
            elif code1 & 0x2 == 2:
                u = (x_max - x0) / (x1 - x0)
                y0 = round(y0 + u * (y1 - y0))
                x0 = x_max
            elif code1 & 0x1 == 1:
                u = (x_min - x0) / (x1 - x0)
                y0 = round(y0 + u * (y1 - y0))
                x0 = x_min
    else:
        u1, u2 = 0, 1
        dx = x1 - x0
        dy = y1 - y0
        p = [-dx, dx, -dy, dy]
        q = [x0 - x_min, x_max - x0, y0 - y_min, y_max - y0]
        for pk, qk in zip(p, q):
            able, u1, u2 = test(pk, qk, u1, u2)
            if able == False:
                return []
        x1 = round(x0 + u2 * dx)
        y1 = round(y0 + u2 * dy)
        x0 = round(x0 + u1 * dx)
        y0 = round(y0 + u1 * dy)
        return [(x0, y0), (x1, y1)]

# if __name__ == '__main__':
