import unittest
from  imei import imei
import cv2


class MyTestCase(unittest.TestCase):
    def test_dime(self):
        gime = imei()
        image = cv2.imread("test_image/imei.jpg")
        ret = gime.imei(image)
        self.assertEqual('862745037134951', ret[0])
        self.assertEqual('862745037209746', ret[1])

    def test_dime2(self):
        gime = imei()
        image = cv2.imread("d:/1/10/6.png")
        ret = gime.imei(image)
        print(ret)

if __name__ == '__main__':
    unittest.main()
