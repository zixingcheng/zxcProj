# -*- coding: utf-8 -*-
"""
Created on  张斌 2020-02-04 18:00:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    图表接口操作类
"""
import sys, string, time
import matplotlib as mpl
import matplotlib.pyplot as plt     #约定俗成的写法plt
from matplotlib.pyplot import MultipleLocator
from matplotlib import font_manager


#绘制曲线
def draw_Curve(datas, marks=None, xlabel="", ylabel="", title="", grid='on', x_major=10, y_major=0.2, smooth=True):
    x = range(len(datas))
    y = datas
    
    # plt.rcParams['figure.figsize'] = (8.0, 4.0)     # 设置figure_size尺寸
    # plt.rcParams['savefig.dpi'] = 150               # 图片像素
    # plt.rcParams['figure.dpi'] = 150                # 分辨率
    fig = plt.figure(figsize=(20, 8), dpi=80)       # 设置figure_size尺寸

    plt.plot(x, y)
    plt.xticks(x)
    plt.yticks(range(int(min(y)), int(max(y)) + 1))
    
    x_major_locator = MultipleLocator(x_major)
    y_major_locator = MultipleLocator(y_major)
    ax = plt.gca()
    ax.xaxis.set_major_locator(x_major_locator)
    ax.yaxis.set_major_locator(y_major_locator)

    plt.plot(x, y)
    if(marks != None):
        plt.scatter(x, marks)
        plt.colorbar()

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

    plt.grid(grid)          #标尺，on：有，off:无。
    return plt
    

if __name__ == '__main__':
    datas1 =[36.01, 35.72, 36.55, 36.06, 36.04, 36.12, 36.12, 36.01, 35.8, 35.76, 36.0, 36.19, 36.13, 36.07, 35.98, 35.9, 36.01, 36.08, 36.16, 36.3, 36.41, 36.35, 36.28, 36.2, 36.12, 36.09, 36.05, 36.07, 36.1, 36.15, 36.27, 36.2, 36.15, 36.14, 36.13, 36.18, 36.22, 36.19, 36.16, 36.08, 36.06, 36.03, 36.07, 36.08, 36.11, 36.08, 36.08, 36.06, 36.0, 35.95, 35.91, 35.92, 36.01, 36.03, 36.04, 36.04, 36.03, 36.02, 36.01, 35.95, 35.95, 35.97, 36.02, 36.02, 36.01, 36.02, 36.02, 36.02, 36.06, 36.07, 36.15, 36.25, 36.32, 36.27, 36.23, 36.21, 36.2, 36.1, 36.03, 36.06, 36.09, 36.17, 36.28, 36.33, 36.31, 36.28, 36.23, 36.29, 36.27, 36.24, 36.2, 36.12, 36.14, 36.13, 36.16, 36.22, 36.28, 36.3, 36.4, 36.37, 36.47, 36.57, 36.68, 36.82, 36.76, 36.61, 36.6, 36.71, 36.84, 36.84, 36.79, 36.73, 36.73, 36.79, 36.83, 36.81, 36.83, 36.81, 36.77, 36.8, 36.86, 36.87, 36.98, 37.06, 37.2, 37.14, 37.03, 36.95, 36.94, 37.0, 37.03, 37.0, 36.98, 37.0, 37.01, 37.02, 37.09, 37.12, 37.21, 37.3, 37.33, 37.4, 37.48, 37.54, 37.32, 37.29, 37.21, 37.13, 37.12, 37.14, 37.14, 37.15, 37.18, 37.17, 37.11, 37.05, 37.01, 36.95, 37.02, 37.05, 37.1, 37.18, 37.17, 37.1, 37.1, 37.08, 37.01, 36.97, 36.96, 36.93, 36.8, 36.82, 36.84, 36.9, 36.91, 36.92, 36.92, 36.91, 36.88, 36.83, 36.83, 36.85, 36.92, 36.97, 37.06, 37.1, 37.13, 37.11, 37.06, 36.97, 37.0, 37.03, 37.04, 37.0, 36.94, 36.88, 36.88, 36.9, 36.94, 36.94, 36.9, 36.87, 36.86, 36.81, 36.76, 36.7, 36.68, 36.7, 36.75, 36.81, 36.83, 36.79, 36.75, 36.73, 36.76, 36.79, 36.8, 36.84, 36.85, 36.85, 36.84, 36.81, 36.72, 36.7, 36.7, 36.69, 36.69, 36.65, 36.57, 36.56, 36.59, 36.7, 36.78, 36.78, 36.63, 36.67, 36.71, 36.71, 36.71]
    datas2 = [10.09, 10.1, 10.13, 10.35, 10.46, 10.20, 9.8, 9.9, 10.3, 10.6, 10.99]

    draw_Curve(datas1, xlabel="Time(s)", ylabel="Price($)", title="Test Datas")
    plt.show()
    
