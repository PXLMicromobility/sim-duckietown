import numpy as np
import os
import shutil

from PIL import Image


class Logger:
    def __init__(self, location):
        self.location = location
        self.images_folder = f'{self.location}/images'

        # TODO: mkdir if needed
        # We currently remove the dir and re-make one
        if os.path.exists(self.location):
            shutil.rmtree(self.location)

        os.makedirs(self.images_folder)

    def writecsv(self, name: str, data: dict):
        path = f'{self.location}/{name}'

        if not os.path.isfile(path):
            print('Creating csv file')
            csv = open(path, 'w')
            csv.write('vel_left,vel_right,joy_x,joy_y,timestamp')
        else:
            csv = open(path, 'a')

        csv.write(f"{data['vel_left']},{data['vel_right']},{data['joy_x']},{data['joy_y']},{data['timestamp']}")

        csv.close()

    def writeimg(self, name: str, img: np.ndarray):
        path = f'{self.location}/images/{name}'

        img = Image.fromarray(img)
        img.save(path)
