# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 20:23:44 2019

@author: acam
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

cT0 = 2
k1A = 5
k2A = 2
k3B = 10
k4C = 5

def equations(V, F):
   
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
    
FA0 = 5
FB0 = 5   

F0 = np.array([FA0, FB0, 0, 0, 0, 0])
Vspan = np.linspace(0, 10, 51)

F = solve_ivp(equations, [0 , 10], F0)

ax = plt.figure().add_subplot(111) 

for i in np.arange(len((F.y))):
    ax.plot(F.t, F.y[i])

plt.xlabel('Volume')
plt.ylabel('Flow')
plt.legend('ABCDEF', loc = 'best')
plt.tight_layout()
plt.axis('tight')