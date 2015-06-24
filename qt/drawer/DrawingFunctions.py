from PyQt4 import QtCore, QtGui

def svgColorToQtColor(svgColor):
    r, g, b = 255, 255, 255 
    if svgColor[0]!='#':
        print "Unknown svg color: %s"%svgColor
    elif len(svgColor)==4:
        r = int(255.0/16*double(int(svgColor[1],16))) 
        g = int(255.0/16*double(int(svgColor[2],16))) 
        b = int(255.0/16*double(int(svgColor[3],16))) 
    elif len(svgColor)==7:
        r = int(svgColor[1:3],16) 
        g = int(svgColor[3:5],16) 
        b = int(svgColor[5:7],16)
    else:
        print "Unknown svg color: %s"%svgColor
    return QtGui.QColor(r, g, b)
   