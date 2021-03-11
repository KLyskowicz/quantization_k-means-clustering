import random
import os
import numpy as np
from center import Center
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Center_coordinator(object):

    def __init__(self, center_amount, min_x, min_y, max_x, max_y, data, path, name='x'):
        self.data = data
        self.dataX = []
        self.dataY = []
        self.path = path
        self.name = name
        self.center_amount = center_amount
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y
        self.last_error = 0
        self.last_error_for_epo = 0
        self.centers = []
        self.centers_best_begin = []

    def new_xy(self):
        self.centers.clear()
        self.centers = [ Center( random.uniform(self.min_x, self.max_x), random.uniform(self.min_y, self.max_y) ) for i in range(self.center_amount) ]
        name2 = os.path.join(self.path, str(self.name) + ".csv")
        centerXY = open(name2,"w+")
        for center in self.centers:
            centerXY.write(str(center.get_x()) + ',' + str(center.get_y()) + '\n')
        centerXY.close

    def allocate_data(self):
        for one_data in self.data:
            distance = []
            for center in self.centers:
                distance.append( center.get_distance(one_data) )
            self.centers[ np.argmin(distance, axis=0) ].data.append(one_data)

    def clear_center_data(self):
        for center in self.centers:
            center.data.clear()

    def update_centers(self):
        for center in self.centers:
            center.update_xy()

    def save_centers_xy(self):
        name2 = os.path.join(self.path, str(self.name) + ".csv")
        fromFile = np.loadtxt(name2, delimiter=',')
        self.centers_best_begin = fromFile[:,0:2]

    def get_centers_error(self):
        error = 0
        for center in self.centers:
            error += center.get_error()
        return error/len(self.data)

    def start_mach(self, experiments_amount, epoches):
        for i in range(experiments_amount):
            self.new_xy()
            for epo in range(epoches):
                self.clear_center_data()
                self.allocate_data()
                self.update_centers() 
                new_error = self.get_centers_error()
                if (self.last_error_for_epo - 0.00001 < new_error) and (self.last_error_for_epo != 0):
                    break
                self.last_error_for_epo = new_error
            self.last_error_for_epo = 0
            new_error = self.get_centers_error()
            if (self.last_error > new_error) or (self.last_error == 0):
                last_error2 = self.last_error
                self.last_error = new_error
                self.save_centers_xy()
        self.set_best_centers_xy()

    def set_best_centers_xy(self):
        self.centers.clear()
        self.centers = [ Center( XY[0], XY[1] ) for XY in self.centers_best_begin ]

    def animate(self, epoches, name):
        Writer = animation.writers['ffmpeg']
        writer = Writer(fps=2, metadata=dict(artist='Me'), bitrate=1800)
        self.dataX = [one_data[0] for one_data in self.data]
        self.dataY = [one_data[1] for one_data in self.data]
        fig, ax1 = plt.subplots()
        ln, = plt.plot([], [], 'ro')
        def init():
            ax1.set_xlim(-15, 15)
            ax1.set_ylim(-15, 15)
            ax1.scatter(self.dataX, self.dataY, color='blue')
            return ln,
        def animate_points(frame):
            xs2 = [center.x for center in self.centers]
            ys2 = [center.y for center in self.centers]
            ln.set_data(xs2, ys2)
            self.clear_center_data()
            self.allocate_data()
            self.update_centers()
            return ln
        ani = animation.FuncAnimation(fig, animate_points, frames=np.arange(0, epoches).tolist(), init_func=init)
        name1 = os.path.join(self.path, str(name) + ".mp4")
        ani.save(name1, writer=writer)
        name2 = os.path.join(self.path, str(name) + ".txt")
        error_save = open(name2,"w+")
        error_save.write(str( round( self.get_centers_error(), 6 ) ))
        error_save.close()

    def print_center_and_data(self):
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Wykres grupowania punktów')
        for center in self.centers:
            plt.scatter(center.get_dat_x(), center.get_dat_y())
            plt.scatter(center.get_x(), center.get_y(), color='r', marker='^')
        plt.show()

    