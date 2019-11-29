import numpy as np
import os
import shutil

from zipfile import ZipFile
from PIL import Image
from io import StringIO

import pandas as pd


class Logger:
    def __init__(self, location: str, begin_index: int = 0):
        self.location = location
        self.images_folder = f'{self.location}/images'

        # TODO: mkdir if needed
        # We currently remove the dir and re-make one
        if os.path.exists(self.location):
            shutil.rmtree(self.location)

        os.makedirs(self.images_folder)

        self._index = self._index_generator(begin_index)

        self.has_recorded = False

    def zip_exists(self) -> bool:
        return os.path.exists(f'{self.location}.zip')

    @staticmethod
    def _index_generator(begin_index: int):
        index = begin_index
        while True:
            yield index
            index += 1

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
        if overwrite or not self.zip_exists():
            mode = 'w'
        else:
            mode = 'a'

        with ZipFile(f'{self.location}.zip', mode=mode) as zf:
            for item in os.listdir(self.location):
                real_path = os.path.join(self.location, item)

                if item.endswith('.csv'):
                    if item in zf.namelist():
                        # Combine the two csv files into one
                        csv_in_zip = StringIO(str(zf.read(item), 'utf-8'))

                        df = pd.read_csv(csv_in_zip)
                        
                        # We append the new data to the old one in the old file
                        # TODO: this does write the new data first and then adds the new data :/
                        df.to_csv(real_path, mode='a+', header=False, index=False)

                    # Overwrite the file, create if it doesn't exist yet
                    with zf.open(item, 'w') as csv_file:
                        csv_file.write(bytes(pd.read_csv(real_path).to_string(), 'utf-8'))
                else:
                    try:
                        # We got a folder (images folder)
                        for image in os.listdir(real_path):
                            zf.write(os.path.join(self.location, item, image), f'images/{image}')
                    except Warning:
                        pass
