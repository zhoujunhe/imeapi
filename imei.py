import cv2
import numpy
import re
from paddleocr import PaddleOCR


class imei:
    def __init__(self,paddocr=None):
        if paddocr:
            self.paddocr = paddocr
        else:
            self.paddocr = PaddleOCR(use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory
        self.re = re.compile('\d{15,17}')
        self.reImei = re.compile('(IMEI|IMEI1|IMEI2|IME11|IME12|IME1|IME|MEI0|ME10|ME12|^|[^0-9]+)(\d{15,17})($|/)')
        #考虑imei分成两行情况
        self.reImei21 = re.compile('(IMEI|IMEI1|IMEI2|IME11|IME12|IME1|IME|MEI0|ME10|ME12|^|[^0-9]+)(\d{12,14}$)')
        self.reImei22 = re.compile('^\d{1,3}$')

    def run(self,image):
        """
        调用ocr识别串号
        :param image:
        :return:
        """
        rows, cols, _ = image.shape
        # 检测是否可以进行90度旋转
        if cols > rows:
            image = cv2.transpose(image)
            image = cv2.flip(image, 1)
        return self.paddocr.ocr(image, cls=True)

    def __Rotation(self,image,ocrlist):
        '''
        对图片安识别出来方向进行旋转
        :param image: 图片
        :param ocrlist:ocr识别结果集
        :return:旋转后图片
        '''
        rows, cols, _ = image.shape
        bin_image = numpy.zeros((rows, cols), numpy.uint8)
        for line in ocrlist:
            box = numpy.int0(numpy.array((line[0])))
            cv2.drawContours(bin_image, [box], 0, (255), 2)

        # 找出角度
        contours, hierarchy = cv2.findContours(bin_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        list_angle = [cv2.minAreaRect(c)[2] for c in contours]
        # 旋转
        if len(list_angle) > 0:
            # 求出最接近角度
            hist = numpy.histogram(numpy.array(list_angle), 3)
            max_index = numpy.argmax(hist[0])
            list_subangle = [x for x in list_angle if x >= hist[1][max_index] and x <= hist[1][max_index + 1]]
            angle = numpy.mean(numpy.array(list_subangle))
            if (angle < -45): angle = angle + 90
            # 旋转
            M = cv2.getRotationMatrix2D((rows / 2, cols / 2), angle, 1)
            image = cv2.warpAffine(image, M, (cols, rows))

        return image

    def __dobule_imei(self,ocrlist):
        '''
        识别出双imei和imei换成两行的
        :param ocrlist: ocr识别结果集
        :return:
        '''
        ret = []
        for line in ocrlist:
            groupImei = self.reImei.search(line[1][0])  # 检测是否有imei号
            if groupImei:  # 有加入list
                ret.append(groupImei.group(2))
        # 没有单行的imei号，查找双行imei号
        if len(ret) == 0:
            size = len(ocrlist)
            for i in range(size - 1):
                groupImei21 = self.reImei21.search(ocrlist[i][1][0])  # 检测是否有imei号第一行
                groupImei22 = self.reImei22.search(ocrlist[i + 1][1][0])  # 检测是否有imei号第二行
                if groupImei21 and groupImei22:  # 找出两行一起出现的
                    imei = groupImei21.group(2) + groupImei22.group()
                    if len(imei) >= 15 and len(imei) <= 17:
                        ret.append(imei)
                        i = i + 1
        return ret


    def imei(self,image):
        '''
        识别出imei号
        :param image: 图片
        :return: list
        '''
        result=self.run(image)
        ret = self.__dobule_imei(result)
        if len(ret)==0:
            image = self.__Rotation(image,result)
            result =self.run(image)
            ret = self.__dobule_imei(result)
        return ret