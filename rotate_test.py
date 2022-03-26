import unittest
from rotate import rotate
import cv2
from common import getFileBuff
import numpy

class MyTestCase(unittest.TestCase):
    def test_rotate(self):
        #buff = getFileBuff("https://aidatasets.igooma.cn/StaticFiles/a.jpg")
        #str_encode = numpy.frombuffer(buff, numpy.uint8)
        #image = cv2.imdecode(str_encode, cv2.IMREAD_COLOR)
        image = cv2.imread("/1/imei/1602905479760657.jpg")
        reimg = rotate(image)
        cv2.namedWindow('reimg', cv2.WINDOW_NORMAL)
        cv2.imshow("reimg", reimg)
        cv2.waitKey(0)






if __name__ == '__main__':
    unittest.main()
