import unittest
from PIL import Image
import numpy
from logger import Logger
import os


class SimulationTester(unittest.TestCase):

    def setUp(self):
        self.sut = Logger("tests/test_images")

    def test_writeimg(self):
        img = Image.open("tests/100.jpeg")
        nimg = numpy.array(img)
        
        with self.subTest("creates_new_image"):
            self.sut.writeimg("test1.jpeg", nimg)
            self.assertTrue(os.path.exists("tests/test_images/images/test1.jpeg"))
        
        values = ["2323", ["dzadd", "aezd", "qaa"], 10, [232, 2344, 424, 2232], True, [True, True, False, True, False], 10.0, [10.0, 0.1, 2.2, 3.34]]

        for v in values:
            with self.subTest(f"raises_type_exception_on_invalid_value_type_{type(v)}"):
                with self.assertRaises(TypeError):
                    self.sut.writeimg("test1.jpeg", v)
        
    def test_writecsv(self):
        
        pass
