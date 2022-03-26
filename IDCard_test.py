import unittest
import cv2
from IDCard import IDCard


class MyTestCase(unittest.TestCase):
    def test_face(self):
        idc = IDCard()
        image = cv2.imread("test_image/face.png")
        ret = idc.face(image)
        print(ret)
        self.assertEqual(ret["name"], "刘新")
        self.assertEqual(ret["num"],'450721199407180125')

    def test_back(self):
        idc = IDCard()
        image = cv2.imread("test_image/back.jpg")
        ret = idc.back(image)
        print(ret)
        self.assertEqual(ret["start_date"], "2016.02.15")
        self.assertEqual(ret["end_date"], '长期')

    def test_face2(self):
        idc = IDCard()
        image = cv2.imread(r"d:/1/2/555.JPG")
        ret = idc.face(image)
        print(ret)



if __name__ == '__main__':
    unittest.main()
