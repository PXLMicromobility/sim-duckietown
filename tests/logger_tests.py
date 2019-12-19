import unittest
from PIL import Image
import numpy
from logger import Logger
import os, shutil, xmlrunner



class SimulationTester(unittest.TestCase):

    def setUp(self):
        if os.path.exists('tests/test'):
            shutil.rmtree("tests/test")
        
        self.sut = Logger("tests/test")

    def test_writeimg(self):
        img = Image.open("tests/test_images/100.jpeg")
        nimg = numpy.array(img)
        
        with self.subTest("creates_new_image"):
            self.sut.writeimg("test1", nimg)
            self.assertTrue(os.path.exists("tests/test/images/test1.jpg"))
        
        values = ["2323", ["dzadd", "aezd", "qaa"], 10, [232, 2344, 424, 2232], True, [True, True, False, True, False], 10.0, [10.0, 0.1, 2.2, 3.34]]

        for v in values:
            with self.subTest(f"raises_type_exception_on_invalid_value_type_{type(v)}", type=type(v), value=v):
                with self.assertRaises(TypeError):
                    self.sut.writeimg("test1", v)
        
    def test_writecsv(self):
        with self.subTest("creates_csv"):
            self.sut.writecsv("test", {'vel_left': 0.00, 'vel_right': 0.10, 'joy_x': 1.00, 'joy_y': 1.01, 'index': 0})
            self.assertTrue(os.path.exists("tests/test/test.csv"))
        
        csv_content = None
        
        with open("tests/test/test.csv", "r") as f:
            csv_content = f.readlines()
        
        values = ['vel_left', 'vel_right', 'joy_x', 'joy_y', 'index']
        
        for value in values:
            with self.subTest(f"newly_created_csv_has_{value}_in_header"):
                self.assertTrue(value in csv_content[0])
        
        
    def tearDown(self):
        if os.path.exists('tests/test'):
            shutil.rmtree("tests/test")
        
        self.sut = None

if __name__ == '__main__':
    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output='test-reports'),
        # these make sure that some options that are not applicable
        # remain hidden from the help menu.
        failfast=False, buffer=False, catchbreak=False)