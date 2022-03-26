import unittest
import cv2
from imei import imei
from paddleocr import PaddleOCR


class MyTestCase(unittest.TestCase):
    def test_something(self):
        img_path = 'test_image/imei.jpg'
        img_path2 = 'test_image/imei2.jpg'
        image = cv2.imread(img_path)
        pocr = PaddleOCR(use_angle_cls=True, lang="ch")

        ime = imei(pocr)
        ret = ime.run(image)
        for line in ret:
            print(line)
        image = cv2.imread(img_path2)
        ret = ime.run(image)
        for line in ret:
            print(line)



if __name__ == '__main__':
    unittest.main()
