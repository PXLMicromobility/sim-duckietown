import numpy as np
import os
import shutil

from zipfile import ZipFile
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

        self._index = self._index_generator()

        self.has_recorded = False

    def _index_generator(self):
        index = 0
        while True:
            yield index
            index += 1

    def next_index(self):
        return next(self._index)

    def writecsv(self, name: str, data: dict):
        if not self.has_recorded:
            self.has_recorded = True

        path = f'{self.location}/{name}'

        if not os.path.isfile(path):
            print('Creating csv file')
            csv = open(path, 'w')
            csv.write('vel_left,vel_right,joy_x,joy_y,index\n')
        else:
            csv = open(path, 'a')

        csv.write(f"{data['vel_left']},{data['vel_right']},{data['joy_x']},{data['joy_y']},{data['index']}\n")

        csv.close()

    def writeimg(self, name: str, img: np.ndarray):
        if not self.has_recorded:
            self.has_recorded = True

        path = f'{self.location}/images/{name}'

        img = Image.fromarray(img)
        img.save(path)

    def log_to_zip(self):
        with ZipFile(f'{self.location}.zip', 'w') as zf:
            for item in os.listdir(self.location):
                if item.endswith('.csv'):
                    zf.write(os.path.join(self.location, item), item)
                else:
                    # We got a folder (images folder)
                    for image in os.listdir(os.path.join(self.location, item)):
                        zf.write(os.path.join(self.location, item, image), f'images/{image}')
