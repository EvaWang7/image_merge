import cv2
import os
import numpy as np
import binascii
import crcmod.predefined
import crc16



def find_lcsubstr(s1, s2):
    m = [[0 for i in range(len(s2) + 1)] for j in range(len(s1) + 1)]
    mmax = 0
    p = 0
    for i in range(len(s1)):
        for j in range(len(s2)):
            if s1[i] == s2[j]:
                m[i + 1][j + 1] = m[i][j] + 1
                if m[i + 1][j + 1] > mmax:
                    mmax = m[i + 1][j + 1]
                    p = i + 1
    return s1[p-mmax:p],p-mmax,mmax


image_list = os.listdir('/Users/evawang/Desktop/untitled/image2')
dict = {}
all_crc16_list = []
for image in sorted(image_list):
    img = cv2.imread(os.path.join('/Users/evawang/Desktop/untitled/image2',image))
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    crc16_list = []
    for l in gray:
        crc16_list.append(crc16.crc16xmodem(l))
    dict[image]= crc16_list
    all_crc16_list.append(crc16_list)


final_img = []
first_img = cv2.imread(os.path.join('/Users/evawang/Desktop/untitled/image2', sorted(image_list)[0]))
final_img.extend(first_img)
for i in range(len(all_crc16_list)):
    crc16_list_1 = all_crc16_list[i]
    if i+2>len(all_crc16_list):
        break
    else:
        crc16_list_2 = all_crc16_list[i+1]
        longest_common_substring, img1_cut_length,length = find_lcsubstr(crc16_list_1,crc16_list_2)
        if length == 0:
            continue
        img1 = cv2.imread(os.path.join('/Users/evawang/Desktop/untitled/image2', sorted(image_list)[i]))
        new_image_1 = img1[:img1_cut_length,:,:]
        img2 = cv2.imread(os.path.join('/Users/evawang/Desktop/untitled/image2', sorted(image_list)[i+1]))
        idx = crc16_list_2.index(longest_common_substring[0])
        new_image_2 = img2[crc16_list_2.index(longest_common_substring[0])+length:, :,:]
        final_img.extend(new_image_2)
cv2.imwrite('final.jpg', np.array(final_img))



