import unittest
from PIL import Image
import numpy
from logger import Logger
import os
import xmlrunner


class SimulationTester(unittest.TestCase):

    def setUp(self):
        self.sut = Logger("tests/test")

    def test_writeimg(self):
        img = Image.open("tests/test_images/100.jpeg")
        nimg = numpy.array(img)
        
        with self.subTest("creates_new_image"):
            self.sut.writeimg("test1", nimg)
            self.assertTrue(os.path.exists("tests/test/images/test1.jpeg"))
        
        values = ["2323", ["dzadd", "aezd", "qaa"], 10, [232, 2344, 424, 2232], True, [True, True, False, True, False], 10.0, [10.0, 0.1, 2.2, 3.34]]

        for v in values:
            with self.subTest(f"raises_type_exception_on_invalid_value_type_{type(v)}"):
                with self.assertRaises(TypeError):
                    self.sut.writeimg("test1", v)
        
    def test_writecsv(self):
        with self.subTest("creates_csv"):
            self.sut.writecsv("test", {'vel_left': 0.00, 'vel_right': 0.10, 'joy_x': 1.00, 'joy_y': 1.01, 'index': 0})
            self.assertTrue(os.path.exists("tests/test/test.csv"))
        