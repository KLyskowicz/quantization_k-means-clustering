import random
import os
import numpy as np
import matplotlib.pyplot as plt
from center_coordinator import Center_coordinator

def make_group_of_points(data_amount, centers, radius):
    for_one_center = int(data_amount/len(centers))
    data = []
    for center in centers:
        for i in range(for_one_center):
            if i<for_one_center*0.8:
                data.append( [ random.uniform( center[0]-0.5*radius, center[0]+0.5*radius ), random.uniform( center[1]-0.5*radius, center[1]+0.5*radius ) ] )
            else:
                data.append( [ random.uniform( center[0]-radius, center[0]+radius ), random.uniform( center[1]-radius, center[1]+radius ) ] )
    return data


X_min = -8
Y_min = -8
X_max = 8
Y_max = 5
Data_amount = 750
Centers_amount = 100
Radius = 3

Experiments_amount = 3
Epoches_of_mach = 30
Epoches_animate = 50

if not os.path.exists('out'):
    os.makedirs('out')
Path = os.path.join(os.getcwd(), 'out')

# data from file
fromFile = np.loadtxt(os.path.dirname(os.path.realpath(__file__)) + '\\' + 'data.csv', delimiter=',')
Data = fromFile[:,0:2]

# random data
# Data = make_group_of_points(Data_amount, Centers, Radius)
# Data = []
# x = 10
# for i in range(int(len(data)/x)):
#     Data.append(data[i*x])

centers = Center_coordinator(Centers_amount, X_min, Y_min, X_max, Y_max, Data, Path)
centers.start_mach(Experiments_amount, Epoches_of_mach)
centers.animate(Epoches_animate, 'name')
