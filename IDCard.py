import re
from paddleocr import PaddleOCR
import cv2



class IDCard:

    def __init__(self,paddocr=None):
        if paddocr:
            self.paddocr = paddocr
        else:
            self.paddocr = PaddleOCR(use_angle_cls=True, lang="ch")
        self.reName = re.compile('(姓名|姓|名)([\u4e00-\u9fa5]{2,})|([\u4e00-\u9fa5]{2,})(姓名|姓|名)')
        self.reSex = re.compile('(性别|性|别)(男|女)')
        self.reNationality = re.compile('(民族|民|族)(汉|满|蒙古|回|藏|维吾尔|苗|彝|壮|布依|侗|瑶|白|土家|哈尼|哈萨克|傣|黎|傈僳|佤|畲|高山|拉祜|水|东乡|纳西|景颇|柯尔克孜|土|达斡尔|仫佬|羌|布朗|撒拉|毛南|仡佬|锡伯|阿昌|普米|朝鲜|塔吉克|怒|乌孜别克|俄罗斯|鄂温克|德昂|保安|裕固|京|塔塔尔|独龙|鄂伦春|赫哲|门巴|珞巴|基诺族)')
        self.reBirth = re.compile('\d{4}年\d{1,2}月\d{1,2}日')
        self.reNum = re.compile('(\d{6})(\d{4})(\d{2})(\d{2})(\d{3})([0-9]|X)')
        self.reValidDate = re.compile('(\d{4}.\d{1,2}.\d{1,2})-(\d{4}.\d{1,2}.\d{1,2}|长期)')

    def face(self,image):
        rows, cols, _ = image.shape
        # 检测是否可以进行90度旋转
        if rows > cols:
            image_tran = cv2.transpose(image)
            image_tran = cv2.flip(image_tran, 0)
            dicRet =  self.face_i(image_tran)
            if 'name' not in dicRet.keys() or 'num' not in dicRet.keys():
                dicRet = self.face_i(image)
        else:
            dicRet = self.face_i(image)
            if 'name' not in dicRet.keys() or 'num' not in dicRet.keys():
                image_tran = cv2.transpose(image)
                image_tran = cv2.flip(image_tran, 0)
                dicRet = self.face_i(image_tran)
        return dicRet


    def face_i(self,image):
        """
        检测身分证
        :param image:  身分证正面
        """
        dic_ret = {}
        result = self.paddocr.ocr(image, cls=True)
        #一行多列合并成一列
        L = []
        while (len(result) > 0):
            value = result[0]
            result.remove(value)
            i = 0
            line_result = value[1][0]
            while (i < len(result)):
                line = result[i]
                if (line[0][3][1] > value[0][1][1] and line[0][0][1] < value[0][2][1]):
                    result.remove(line)
                    line_result = line_result + line[1][0]
                else:
                    i = i + 1
            L.append(line_result)
        #print(L)
        for line in L:
            groupName = self.reName.search(line)
            groupSex = self.reSex.search(line)
            groupNationality = self.reNationality.search(line)
            groupBirth = self.reBirth.search(line)
            groupNum = self.reNum.search(line)
            if groupName:
                dic_ret["name"] = groupName.group(2) if groupName.group(2) else groupName.group(3)
            elif groupSex:
                dic_ret["sex"] = groupSex.group(2)
            if groupNationality:
                dic_ret["nationality"] = groupNationality.group(2)
            elif groupBirth:
                dic_ret["birth"] = groupBirth.group()
            elif groupNum:
                dic_ret["num"] = groupNum.group()
        return dic_ret

    def back(self,image):
        dic_ret = {}
        result = self.paddocr.ocr(image, cls=True)
        for line in result:
            groupNum = self.reValidDate.search(line[1][0])
            if groupNum:
                dic_ret["start_date"] = groupNum.group(1)
                dic_ret["end_date"] = groupNum.group(2)
        return dic_ret
