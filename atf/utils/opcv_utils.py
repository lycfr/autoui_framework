#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

import cv2
import numpy as np

from atf.commons.logging import log_info
from atf.commons.variable_global import Var


class OpencvUtils(object):

    def __init__(self,action, matchimage):

        self.action = action
        self.baseimage = None
        self.matchimage = matchimage
        self.iszoom = False

    def save_screenshot(self):
        """
        截图
        :return:
        """
        try:
            ocrimg = os.path.join(Var.ROOT, 'OcrImg')
            if not os.path.exists(ocrimg):
                os.makedirs(ocrimg)
            imgname = self.matchimage.split(os.sep)[-1]
            file_path = os.path.join(ocrimg, '{}_{}'.format(self.action, imgname))
            Var.appinstance.save_screenshot(file_path)
            Var.appinstance.save_screenshot(Var.file)
            self.baseimage = file_path
            return self.baseimage
        except Exception as e:
            raise e

    def extract_minutiae(self):
        """
        提取特征点
        :return:
        """
        if os.path.exists(self.matchimage):
            self.baseimage = cv2.imread(self.baseimage)
            self.matchimage = cv2.imread(self.matchimage)

            view_height = Var.appinstance.get_window_size()['height']#获取手机屏幕的高度
            image_height = self.baseimage.shape[0]#图像的大小可以通过其shape属性来获取，shape返回的是一个tuple元组，第一个元素表示图像的高度，第二个表示图像的宽度，第三个表示像素的通道数。
            #print("image_height",image_height)
            if view_height * 2 == image_height:
                self.iszoom = True

        else:
            raise FileExistsError(self.matchimage)
        '''
        1.使用SIFT算法检测特征点、描述符
        '''
        # 创建一个SURF对象
        #SURF将SIFT中的Laplacian of a Gaussian（LOG）用一个方框滤波（box filter）代替。opencv2:cv2.SURF，opencv3:cv2.xfeatures2d.SURF_create()
        #大的值输出的数量比较少但是它们更为突出，相比之下输出较小的值虽然多但是不够突出（就是与普通差别不够大）
        min_hessian = 400
        surf = cv2.xfeatures2d.SURF_create(min_hessian)
        # SIFT对象会使用Hessian算法检测关键点，并且对每个关键点周围的区域计算特征向量。该函数返回关键点的信息和描述符
        keypoints1, descriptor1 = surf.detectAndCompute(self.baseimage, None)
        keypoints2, descriptor2 = surf.detectAndCompute(self.matchimage, None)

        if descriptor2 is None:
            return None
        '''
        2、FLANN匹配
        '''
        # 特征点匹配
        matcher = cv2.FlannBasedMatcher()
        matchePoints = matcher.match(descriptor1, descriptor2)#(self, queryDescriptors, trainDescriptors, mask=None)
        # matchePoints = matcher.knnMatch(descriptor1, descriptor2, k=2)#(self, queryDescriptors, trainDescriptors, k, mask=None, compactResult=None)
        '''
        matchePoints
        queryIdx：测试图像的特征点描述符的下标（第几个特征点描述符），同时也是描述符对应特征点的下标。
        trainIdx：样本图像的特征点描述符下标,同时也是描述符对应特征点的下标。
        distance：代表这怡翠匹配的特征点描述符的欧式距离，数值越小也就说明俩个特征点越相近
        .pt:关键点坐标，.angle：表示关键点方向，.response表示响应强度，.size:标书该点的直径大小
        '''
        #提取强匹配特征点
        minMatch = 1
        maxMatch = 0
        for i in range(len(matchePoints)):
            if minMatch > matchePoints[i].distance:
                minMatch = matchePoints[i].distance
            if maxMatch < matchePoints[i].distance:
                maxMatch = matchePoints[i].distance
        if minMatch > 0.2:
            return None
        # #获取排列在前边的几个最优匹配结果
        MatchePoints = []
        for i in range(len(matchePoints)):
            if matchePoints[i].distance == minMatch:
                keypoint = keypoints1[matchePoints[i].queryIdx]
                x, y = keypoint.pt
                if self.iszoom:
                    x = x / 2.0
                    y = y / 2.0
                # keypoints1 = [keypoint]
                dmatch = matchePoints[i]

                dmatch.queryIdx = 0

                MatchePoints.append(dmatch)
                # print("MatchePoints.append(dmatch)",MatchePoints)


        # 绘制最优匹配点
        img_matches = np.empty((max(self.baseimage.shape[0], self.matchimage.shape[0]), self.baseimage.shape[1] + self.matchimage.shape[1], 3), dtype=np.uint8)

        outImg = None
        # outImg = cv2.drawMatches(self.baseimage, keypoints1, self.matchimage, keypoints2, MatchePoints, outImg, matchColor=(0, 255, 0),
        #                          flags=cv2.DRAW_MATCHES_FLAGS_DEFAULT)
        outImg = cv2.drawMatches(self.baseimage, keypoints1, self.matchimage, keypoints2, MatchePoints, img_matches,
                                 matchColor=(0, 255, 0),
                                 flags=cv2.DRAW_MATCHES_FLAGS_DEFAULT)
        cv2.imwrite(Var.file, outImg)
        #print("x",x,",y:",y)
        matchinfo = {
            'x':int(x),
            'y':int(y),
            'ocrimg':outImg
        }
        return matchinfo


from PIL import Image

class CompareImage():

    def calculate(self, image1, image2):
        g = image1.histogram()
        s = image2.histogram()
        assert len(g) == len(s), "error"

        data = []

        for index in range(0, len(g)):
            if g[index] != s[index]:
                data.append(1 - abs(g[index] - s[index]) / max(g[index], s[index]))
            else:
                data.append(1)

        return sum(data) / len(g)


    def split_image(self, image, part_size):
        pw, ph = part_size
        w, h = image.size

        sub_image_list = []

        assert w % pw == h % ph == 0, "error"

        for i in range(0, w, pw):
            for j in range(0, h, ph):
                sub_image = image.crop((i, j, i + pw, j + ph)).copy()
                sub_image_list.append(sub_image)

        return sub_image_list


    def compare_image(self, file_image1, file_image2, size=(256, 256), part_size=(64, 64)):
        '''
        'file_image1'和'file_image2'是传入的文件路径
         可以通过'Image.open(path)'创建'image1' 和 'image2' Image 对象.
         'size' 重新将 image 对象的尺寸进行重置，默认大小为256 * 256 .
         'part_size' 定义了分割图片的大小.默认大小为64*64 .
         返回值是 'image1' 和 'image2'对比后的相似度，相似度越高，图片越接近，达到1.0说明图片完全相同。
        '''

        image1 = Image.open(file_image1)
        image2 = Image.open(file_image2)

        img1 = image1.resize(size).convert("RGB")
        sub_image1 = self.split_image(img1, part_size)

        img2 = image2.resize(size).convert("RGB")
        sub_image2 = self.split_image(img2, part_size)

        sub_data = 0
        for im1, im2 in zip(sub_image1, sub_image2):
            sub_data += self.calculate(im1, im2)

        x = size[0] / part_size[0]
        y = size[1] / part_size[1]

        pre = round((sub_data / (x * y)), 6)
        # print(str(pre * 100) + '%')
        log_info('Compare the image result is:{} ' .format(str(pre)))
        return pre