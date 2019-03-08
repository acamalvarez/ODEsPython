# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 20:17:03 2019

@author: acam
"""

#from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QGridLayout, QLineEdit,
                             QWidget, QLabel, QPushButton)
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

def equations(F, V, cT0, k1A, k2A, k3B, k4C):

    FT = np.sum(F)
    
    cA = F[0]*cT0/FT
    cB = F[1]*cT0/FT
    cC = F[2]*cT0/FT

    r1A = -k1A*cA*cB**2.0
    r2A = -k2A*cA*cB
    r3B = -k3B*cC**2.0*cB
    r4C = -k4C*cC*cA**(2.0/3)
    
    F = [r1A+r2A+(2.0/3)*r4C, 1.25*r1A+0.75*r2A+r3B, -r1A+2*r3B+r4C,
         -1.5*r1A-1.5*r2A-r4C, -0.5*r2A-(5/6)*r4C, -2*r3B]

    return F

class MyWindow(QWidget):

    def __init__(self, parent = None):
        super(MyWindow, self).__init__(parent)
        self.setGeometry(50, 50, 600, 400)
        self.setWindowTitle("Solve ODE System")
#        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.home()

    def home(self):
        
        # Define Font
        font = self.font()
        font.setWeight(75)
        font.setPointSize(10)
        
        ## Create Grid Layout        
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        
        ## Create Labels        
        
        Parameters = QLabel('Parameters', self)
        self.grid.addWidget(Parameters, 0, 0)
#        Parameters.setFont(font)
        
        Labels = ['cT0', 'k1A', 'k2A', 'k3B', 'k4C', 'FA0', 'FB0']
        
        for i in np.arange(len(Labels)):
            if i < Labels.index('FA0'):
                Label = QLabel(Labels[i], self)
                self.grid.addWidget(Label, i+1, 0)
                
            else:
                Label = QLabel(Labels[i], self)               
                self.grid.addWidget(Label, i+2, 0)

        Graph = QLabel('Graph', self)
        self.grid.addWidget(Graph, 0, 10)
#        Graph.setFont(font)
        
        ## Create Line Edit
        
        self.cT0 = QLineEdit("2", self)
        self.grid.addWidget(self.cT0, 1, 1)
        
        self.k1A = QLineEdit("5", self)
        self.grid.addWidget(self.k1A, 2, 1)
        
        self.k2A = QLineEdit("2", self)
        self.grid.addWidget(self.k2A, 3, 1)
        
        self.k3B = QLineEdit("10", self)
        self.grid.addWidget(self.k3B, 4, 1)

        self.k4C = QLineEdit("5", self)
        self.grid.addWidget(self.k4C, 5, 1)
        
        self.FA0 = QLineEdit("5", self)
        self.grid.addWidget(self.FA0, 7, 1)
        
        self.FB0 = QLineEdit("5", self)
        self.grid.addWidget(self.FB0, 8, 1)
        
        ## Create Button for calculations and Restart
        
        self.btn1 = QPushButton("Plot", self)
        self.grid.addWidget(self.btn1, 10, 0)
        
        self.btn2 = QPushButton("Problem", self)
        self.grid.addWidget(self.btn2, 11, 0)
#        
        self.figure = plt.figure(figsize=(30,10)) 
        self.canvas = FigureCanvas(self.figure)     
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.grid.addWidget(self.canvas, 1,2,10,20)
        self.grid.addWidget(self.toolbar, 15,2,1,20)
        
        self.btn1.clicked.connect(self.calculate)
        self.btn2.clicked.connect(self.problem) 
                
        self.problem()

    def problem(self):
        
        plt.cla()
        img = plt.imread('Problem.jpg')
        plt.imshow(img)
        plt.tight_layout()
        plt.axis('off')
        
        self.canvas.draw()
        
    def calculate(self):
        
        cT0 = float(self.cT0.text())
        k1A = float(self.k1A.text())
        k2A = float(self.k2A.text())
        k3B = float(self.k3B.text())
        k4C = float(self.k4C.text())
        FA0 = float(self.FA0.text())
        FB0 = float(self.FB0.text())        
        
        F0 = [FA0, FB0, 0., 0., 0., 0.]
        
        Vspan = np.linspace(0, 10, 51)

        F = odeint(equations, F0, Vspan, args = (cT0, k1A, k2A, k3B, k4C))

        plt.cla()
        self.ax = self.figure.add_subplot(111)     
        self.ax.plot(Vspan, F)
#        self.ax.set_title('Flow vs Volume')
        
        plt.xlabel('Volume')
        plt.ylabel('Flow')
        plt.legend('ABCDEF', loc = 'best')
        plt.tight_layout()
        plt.axis('tight')
        
        self.canvas.draw()
        
      
if __name__ == '__main__':
    import sys
    from PyQt5 import QtWidgets
    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance() 
    main = MyWindow()
    main.show()
    sys.exit(app.exec_())