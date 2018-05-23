#!/usr/bin/python3
# coding: utf-8

# ---- Description ----
""" Map management """

# ---- Imports ----
import copy
import numpy as np
import matplotlib.pyplot as plt


# ---- Class ----
class Plan_Master:
    """ Create and manage maps """
    freeway = 0
    obstacle = 1
    unknown = -1
    point_size = 4

    def __init__(self, position=(0, 0), direction=0, shape=(1, 1)):
        self.plan: list = np.full(shape, Plan_Master.freeway).tolist()
        self.position = position
        self.direction = (direction + 90) % 360

    def save_plan(self, filename):
        img = plt.figure()
        fig = plt.imshow(np.array(self.plan), interpolation='nearest')
        fig.set_cmap('hot')
        plt.axis('off')
        img.savefig(filename, bbox_inches='tight', pad_inches=0, transparent=True)

    def show_plan(self):
        fig = plt.imshow(np.array(self.plan), interpolation='nearest')
        fig.set_cmap('hot')
        plt.axis('off')
        plt.show()

    def treat_mesures(self, datas):
        batch = []
        datas = copy.deepcopy(datas)
        for info in datas:
            batch.append(info)
            batch[-1]['angle'] = (
                    (batch[-1]['angle'] + 360 - self.direction) % 360  # if robot add its direction to mesures
            )
        return batch

    def place_measures(self, datas):
        batch = self.treat_mesures(datas=datas)
        for point in batch:
            self.position = self.add_point(point['distance'], point['angle'])

    def put_point(self, x, y, code):
        """ Put a shift * shift square on map with x - y center """
        shift = self.point_size
        for i in range(x - shift, x + shift + 1):
            for j in range(y - shift, y + shift + 1):
                self.plan[i][j] = code

    def add_point(self, distance, angle):
        relative_x, relative_y = self.calculate_relative(distance, angle)

        new_x = self.position[0]
        new_y = self.position[1]

        point_x = new_x + relative_x
        point_y = new_y + relative_y

        if point_x + self.point_size >= len(self.plan):
            for i in range(len(self.plan), point_x + self.point_size + 1):
                self.plan.append([0] * len(self.plan[0]))
        if point_x - self.point_size < 0:
            for i in range(point_x - self.point_size, 0):
                self.plan.insert(0, [0] * len(self.plan[0]))
            new_x += np.absolute(point_x - self.point_size // 2)

        if point_y - self.point_size < 0:
            y = np.absolute(point_y - self.point_size)
            for i in range(len(self.plan)):
                self.plan[i] = [0] * y + self.plan[i]
            new_y += np.absolute(point_y - self.point_size // 2)
        if point_y + self.point_size >= len(self.plan[0]):
            length = point_y + self.point_size - len(self.plan[0])
            for i in range(len(self.plan)):
                self.plan[i] += [0] * (length + 1)

        point_x = max(0, point_x)
        point_y = max(0, point_y)
        self.put_point(point_x, point_y, 1)
        return new_x, new_y

    def search_pattern(self, datas):
        positions = []
        for point in datas:
            positions.append(self.calculate_relative(point.get('distance'), point.get('angle')))
        for i in range(len(self.plan)):
            for j in range(len(self.plan[i])):
                if self.plan[i][j] not in (0, 5):
                    continue
                valid = 0
                for x, y in positions:
                    try:
                        if self.plan[i + x][j + y] == 0:
                            break
                        else:
                            valid += 1
                    except IndexError:
                        break
                if valid == len(positions):
                    return i, j

    def scan(self, rangemin, rangemax, datas, zero_test=True):
        """ Scan the map """
        datas = copy.deepcopy(datas)
        pred = []
        for i in range(rangemin, rangemax):
            tests = []
            for index in datas:
                tests.append(copy.deepcopy(index))
                tests[-1]['angle'] = (tests[-1]['angle'] + 360 - i) % 360
            coord = self.search_pattern(tests)
            if coord is not None:
                pred.append((coord, i))
                if zero_test:
                    if i == 0:
                        return self.scan(-20, 20, datas, zero_test=False)
        return pred

    def search_position(self, datas):
        datas = copy.deepcopy(datas)
        pred = self.scan(0, 360, datas, zero_test=True)
        resdir = 0
        coord = np.full(shape=2, fill_value=0)
        for prediction in pred:
            coord += np.array(prediction[0])
            resdir += prediction[1]

        try:
            resdir /= len(pred)
            coord = coord // len(pred)
            coord = coord.tolist()
        except ZeroDivisionError:
            resdir = None
            coord = None
        if resdir < 0:
            resdir = (360 + resdir) % 360
        return coord, resdir

    @staticmethod
    def calculate_relative(distance, angle):
        relative_x = int(np.round(np.sin(np.deg2rad(angle)) * distance))
        relative_y = int(np.round(np.cos(np.deg2rad(angle)) * distance))
        return relative_x, relative_y
