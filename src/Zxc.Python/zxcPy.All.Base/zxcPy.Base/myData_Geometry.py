# -*- coding: utf-8 -*-
"""
Created on  张斌 2020-08-19 10:00:00 
    @author: zhang bin
    @email:  zhangbin@qq.com

    自定义数据类型--GEO操作
"""
import sys, string, math
 


# 计算两点距离
def distance(x0, y0, x1, y1):
    dic = math.pow(x0 - x1, 2) + math.pow(y0 - y1, 2)
    dic = math.sqrt(dic)
    return dic
# 计算线长度
def distanceLine(linePoints):
    numPoint = len(linePoints) - 2
    dic = 0
    for x in range(0, numPoint, 2):
        x0 = linePoints[x]
        y0 = linePoints[x + 1]
        x1 = linePoints[x + 2]
        y1 = linePoints[x + 3]
        dic += distance(x0, y0, x1, y1)
    return dic

# 断点(线段)
def breakLines(linePoints, breakDic, deltaDic=0):
    numPoint = len(linePoints) - 2
    _deltaDic = deltaDic
    _breakPoints = []
    _points = []
    for x in range(0, numPoint, 2):
        x0 = linePoints[x]
        y0 = linePoints[x + 1]
        x1 = linePoints[x + 2]
        y1 = linePoints[x + 3]
        _points.append(x0); _points.append(y0);

        # 调用计算断点(线段)
        _deltaDic, points = breakLine(x0, y0, x1, y1, breakDic, _deltaDic)
        _numBreak = len(points)
        if(_numBreak < 1): continue;

        for xx in range(0, _numBreak, 2):
            _x0 = points[xx]; 
            _y0 = points[xx + 1]; 
            _points.append(_x0); _points.append(_y0);
            _breakPoints.append([_x0, _y0, int(len(_points) / 2)])
    _points.append(linePoints[numPoint]); _points.append(linePoints[numPoint + 1]);
    return _breakPoints, _points
# 断点(线段)
def breakLine(x0, y0, x1, y1, breakDic, deltaDic=0):
    points = []
    _deltaDic = deltaDic
    while(True):
        breaks = breakLine_segment(x0, y0, x1, y1, breakDic, _deltaDic)
        x0 = breaks[1]; y0 = breaks[2];
        if(breaks[4] == breakDic):
            points.append(x0); points.append(y0); _deltaDic = 0;
        else: 
            _deltaDic += breaks[0]
            break;
        if(breaks[0] < breakDic):
            _deltaDic += breaks[0]
            break;
    return _deltaDic, points
# 断点(线段-单次)
def breakLine_segment(x0, y0, x1, y1, breakDic, deltaDic=0):
    dic = distance(x0, y0, x1, y1)
    _breakDic = breakDic - deltaDic
    if(dic < _breakDic):
        return dic + deltaDic, None, None, 0, 0
    if(dic - _breakDic < 0.000006):
        return 0, None, None, 0, 0
    
    ratio = _breakDic / dic
    _x = (x1 - x0) * ratio + x0
    _y = (y1 - y0) * ratio + y0
    _dic = dic - _breakDic
    return _dic, _x, _y, _breakDic, _breakDic + deltaDic



if __name__ == '__main__':   
    print(distance(0,0, 1,1))
    print(distanceLine([0,0, 0,1, 0,3, 0,4, 1,4, 4,4 , 4,1, 4,0]))
    print(breakLine(0,0, 0,1, 1))
    print(breakLine(0,0, 1,1, 2))
    print(breakLine(0,0, 1,1, 1, 0.5))
    print(breakLines([0,0, 0,1, 0,3, 0,4, 1,4, 4,4 , 4,1, 4,0], 2, 0))
 