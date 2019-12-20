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
        imgs = []
        nimgs = []

        for i, im in enumerate(os.listdir("tests/test_images")):
            imgs.append(Image.open(f"tests/test_images/{im}"))
            nimgs.append(numpy.array(imgs[i]))
        
        with self.subTest("creates_new_image"):
            for i, nimg in enumerate(nimgs): 
                self.sut.writeimg(f"test{i}", nimg)
                self.assertTrue(os.path.exists(f"tests/test/images/test{i}.jpg"))
        
        values = ["2323", ["dzadd", "aezd", "qaa"], 10, [232, 2344, 424, 2232], True, [True, True, False, True, False], 10.0, [10.0, 0.1, 2.2, 3.34]]

        for v in values:
            with self.subTest(f"raises_type_exception_on_invalid_value_type_{type(v)}", type=type(v), value=v):
                with self.assertRaises(TypeError):
                    self.sut.writeimg("test1", v)
        
    def test_writecsv(self):
        
        test_data = [{'vel_left': 0.00, 'vel_right': 0.10, 'joy_x': 1.00, 'joy_y': 1.01, 'index': self.sut.next_index()}, 
                     {'vel_left': 0.24, 'vel_right': 1.12, 'joy_x': 1.33, 'joy_y': 1.61, 'index': self.sut.next_index()}, 
                     {'vel_left': 1.03, 'vel_right': 0.19, 'joy_x': 1.37, 'joy_y': 1.41, 'index': self.sut.next_index()}]
        
        with self.subTest("creates_csv"):
            for data in test_data:
                self.sut.writecsv("test", data)
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

# coverage run --source=. --omit="*tests*" -m unittest discover -s tests -p "*_tests.py" && coverage xml -i
# python -m xmlrunner discover -s tests -p "*_tests.py" -o "unittest-results"