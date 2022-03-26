import cv2
import numpy
def rotate(src):
    # 腐蚀
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 2))
    Pretreatment = cv2.erode(src, kernel)
    # 灰度图
    Pretreatment = cv2.cvtColor(Pretreatment, cv2.COLOR_BGRA2GRAY)
    # 算子 轮廓提取
    binary = cv2.Canny(Pretreatment, 150, 200)
    # 膨胀
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 8))
    binary = cv2.dilate(binary, kernel)
    rows, cols = binary.shape
    area = rows * cols
    # 轮廓查找
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


    #求符全条件内矩形框角度
    list_angle = [cv2.minAreaRect(c)[2] for c in contours if cv2.contourArea(c)/ area > 0.01]
    if (len(list_angle)==0): return src
    #求出最接近角度
    hist = numpy.histogram(numpy.array(list_angle), 3)
    max_index = numpy.argmax(hist[0])
    list_subangle = [x for x in list_angle if x >= hist[1][max_index] and x <= hist[1][max_index + 1]]
    angle = numpy.mean(numpy.array(list_subangle))
    if (angle < -45): angle = angle + 90
    M = cv2.getRotationMatrix2D((rows / 2, cols / 2), angle, 1)
    src = cv2.warpAffine(src, M, ( cols,rows))

    #检测是否需要90度转
    binary = cv2.warpAffine(binary, M, (cols, rows))
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    index_90=0
    index_0=0
    for c in contours :
        rect = cv2.boundingRect(c)
        if cv2.contourArea(c) / area > 0.01:
            if   rect[3]>rect[2]:
                index_90 = index_90 + 1
            else:
                index_0 = index_0+1
    if index_90>index_0:
        src = cv2.transpose(src)
        src = cv2.flip(src,1)
    return src
