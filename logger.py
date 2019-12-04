import numpy as np
import os
import shutil

from zipfile import ZipFile
from PIL import Image

import pandas as pd


class Logger:
    def __init__(self, location: str):
        self.location = location
        self._zip_name = self.__get_zip_name()
        self.images_folder = f'{self.location}/images'

        # We currently remove the dir and re-make one
        if os.path.exists(self.location):
            shutil.rmtree(self.location)

        os.makedirs(self.images_folder)

        self.__begin_index = self.__get_last_index()
        self._index = Logger._index_generator(self.__begin_index + 1)

        self.has_recorded = False

    def __get_zip_name(self):
        val = 0

        while True:
            if os.path.exists(f'{self.location}_{val}.zip'):
                val += 1
                continue

            return f'{self.location}_{val}.zip'

    def __get_last_index(self) -> int:
        last_int = 0

        if not os.path.exists(self._zip_name):
            return last_int

        with ZipFile(self._zip_name, 'r') as zf:
            for item in zf.namelist():
                if not item.endswith('.jpg'):
                    continue

                name, _ = os.path.splitext(item)

                name = name.split('/')[1]

                try:
                    int(name)
                except:
                    # Name is not an int
                    continue

                if int(name) > last_int:
                    last_int = int(name)

        return last_int

    @staticmethod
    def _index_generator(begin_index: int):
        index = begin_index
        while True:
            yield index
            index += 1

    def zip_exists(self):
        return os.path.exists(self._zip_name)

    def next_index(self):
        return next(self._index)

    def writecsv(self, name: str, data: dict):
        if not self.has_recorded:
            self.has_recorded = True

        path = f'{self.location}/{name}'

        with open(path, 'a+') as csv:
            if not os.path.isfile(path):
                print('Creating csv file')
                csv.write('vel_left,vel_right,joy_x,joy_y,index\n')

            # TODO: check if a row with a given index already exists?
            csv.write(f"{data['vel_left']},{data['vel_right']},{data['joy_x']},{data['joy_y']},{data['index']}\n")

    def writeimg(self, name: str, img: np.ndarray):
        if not self.has_recorded:
            self.has_recorded = True

        path = f'{self.location}/images/{name}'

        img = Image.fromarray(img)
        img.save(path)

    def log_to_zip(self, overwrite: bool = False):
        if not overwrite:
            self._zip_name = self.__get_zip_name()

        with ZipFile(self._zip_name, mode='w') as zf:
            for item in os.listdir(self.location):
                real_path = os.path.join(self.location, item)

                if item.endswith('.csv'):
                    # Overwrite the file, create if it doesn't exist yet
                    with zf.open(item, 'w') as csv_file:
                        csv_file.write(bytes(pd.read_csv(real_path).to_string(), 'utf-8'))
                else:
                    for image in os.listdir(real_path):
                        zf.write(os.path.join(self.location, item, image), f'images/{image}')
